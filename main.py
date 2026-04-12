#!/usr/bin/env python3
"""
Maxwell's Treatise → Python Library Processing Pipeline

This pipeline processes OCR'd JSON files chapter-by-chapter,
maintaining state across API calls to avoid context overload.

Usage:
    python main.py --part data/PART_I_ELECTROSTATICS/ \
                   --arch specs/Part_I_Architecture.md \
                   --output output/maxwell/
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

from state import ProcessingState
from article_extractor import extract_article_markers, concatenate_chapter_text
from api_client import OpenRouterClient
from prompts import build_system_prompt, build_chapter_prompt
from code_generator import generate_module_files


def get_chapter_order(chapter_files: list[Path]) -> list[Path]:
    """
    Sort chapter files in correct order.
    Handles: CHAPTER_I, CHAPTER_II, ..., CHAPTER_XIII
    """
    roman_to_int = {
        'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
        'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10,
        'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14, 'XV': 15
    }
    
    def extract_chapter_num(path: Path) -> int:
        name = path.stem  # CHAPTER_III_ON_ELECTRICAL...
        parts = name.split('_')
        if len(parts) >= 2:
            roman = parts[1]
            return roman_to_int.get(roman, 999)
        return 999
    
    return sorted(chapter_files, key=extract_chapter_num)


def load_architecture_spec(arch_path: Path) -> str:
    """
    Load and optionally compress the architecture specification.
    For very large specs, we extract only the relevant layer mappings.
    """
    if not arch_path.exists():
        print(f"Warning: Architecture spec not found at {arch_path}")
        return ""
    
    content = arch_path.read_text(encoding='utf-8')
    
    # If spec is very large, extract key sections
    if len(content) > 50000:
        # TODO: Implement selective extraction of layer tables
        print(f"Note: Architecture spec is large ({len(content)} chars), using full content")
    
    return content


def process_single_chapter(
    chapter_file: Path,
    arch_spec: str,
    state: ProcessingState,
    client: OpenRouterClient,
    output_dir: Path,
    model: str,
    thinking_budget: int
) -> dict:
    """
    Process a single chapter through the AI pipeline.
    
    Returns the parsed result with articles and state updates.
    """
    # 1. Load chapter JSON
    print(f"  Loading {chapter_file.name}...")
    with open(chapter_file, 'r', encoding='utf-8') as f:
        chapter_pages = json.load(f)
    
    # 2. Pre-extract article markers (deterministic)
    print(f"  Extracting article markers...")
    article_hints = extract_article_markers(chapter_pages)
    print(f"    Found {len(article_hints)} article markers")
    
    # 3. Concatenate chapter text
    chapter_text = concatenate_chapter_text(chapter_pages)
    print(f"    Chapter text: {len(chapter_text)} characters")
    
    # 4. Build prompts
    system_prompt = build_system_prompt()
    user_prompt = build_chapter_prompt(
        arch_spec=arch_spec,
        state=state,
        chapter_name=chapter_file.stem,
        chapter_text=chapter_text,
        article_hints=article_hints
    )
    
    print(f"  Calling API with {model}...")
    print(f"    System prompt: {len(system_prompt)} chars")
    print(f"    User prompt: {len(user_prompt)} chars")
    
    # 5. Call API with extended thinking
    response = client.call_with_thinking(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=model,
        max_tokens=16000,
        thinking_budget=thinking_budget
    )
    
    # 6. Extract content and thinking
    content, thinking = client.extract_content(response)
    
    if thinking:
        print(f"    AI thinking: {len(thinking)} chars")
    
    # 7. Parse JSON from content
    try:
        # Find JSON in response (might have markdown code blocks)
        json_content = content
        if '```json' in content:
            start = content.find('```json') + 7
            end = content.find('```', start)
            json_content = content[start:end].strip()
        elif '```' in content:
            start = content.find('```') + 3
            end = content.find('```', start)
            json_content = content[start:end].strip()
        
        result = json.loads(json_content)
        
    except json.JSONDecodeError as e:
        print(f"  ERROR: Failed to parse JSON response: {e}")
        print(f"  Raw content preview: {content[:500]}...")
        
        # Save raw response for debugging
        debug_file = output_dir / f"debug_{chapter_file.stem}.txt"
        debug_file.write_text(content, encoding='utf-8')
        print(f"  Saved raw response to {debug_file}")
        
        # Return empty result
        result = {
            "chapter": chapter_file.stem,
            "articles": [],
            "state_updates": {},
            "error": str(e)
        }
    
    # 8. Save thinking for analysis (optional)
    if thinking:
        thinking_file = output_dir / "thinking" / f"{chapter_file.stem}_thinking.txt"
        thinking_file.parent.mkdir(parents=True, exist_ok=True)
        thinking_file.write_text(thinking, encoding='utf-8')
    
    return result


def process_treatise(
    part_dir: Path,
    arch_path: Path,
    output_dir: Path,
    model: str = "anthropic/claude-sonnet-4-20250514",
    thinking_budget: int = 10000,
    resume_from: str = None,
    api_key: str = None
):
    """
    Main entry point: Process all chapters in a Part.
    
    Args:
        part_dir: Directory containing CHAPTER_*.JSON files
        arch_path: Path to architecture specification markdown
        output_dir: Where to write generated Python modules
        model: OpenRouter model identifier
        thinking_budget: Token budget for extended thinking
        resume_from: Optional chapter name to resume from
        api_key: OpenRouter API key (or use OPENROUTER_API_KEY env)
    """
    print("=" * 60)
    print("MAXWELL'S TREATISE PROCESSING PIPELINE")
    print("=" * 60)
    
    # Validate inputs
    if not part_dir.exists():
        print(f"ERROR: Part directory not found: {part_dir}")
        sys.exit(1)
    
    # Get API key
    api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: No API key provided. Set OPENROUTER_API_KEY or use --api-key")
        sys.exit(1)
    
    # Initialize client
    client = OpenRouterClient(api_key=api_key)
    
    # Load architecture spec
    print(f"\nLoading architecture spec from {arch_path}...")
    arch_spec = load_architecture_spec(arch_path)
    print(f"  Loaded {len(arch_spec)} characters")
    
    # Initialize or load state
    state_file = output_dir / "processing_state.json"
    if resume_from and state_file.exists():
        print(f"\nResuming from checkpoint...")
        state = ProcessingState.load(state_file)
        print(f"  Loaded state with {len(state.processed_chapters)} processed chapters")
    else:
        print(f"\nInitializing fresh state...")
        state = ProcessingState(part=part_dir.name)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get chapter files in order
    chapter_files = list(part_dir.glob("CHAPTER_*.JSON")) + \
                    list(part_dir.glob("CHAPTER_*.json"))
    chapter_files = get_chapter_order(chapter_files)
    
    print(f"\nFound {len(chapter_files)} chapter files:")
    for cf in chapter_files:
        print(f"  - {cf.name}")
    
    # Process each chapter
    skipping = resume_from is not None
    
    for chapter_file in chapter_files:
        chapter_name = chapter_file.stem
        
        # Handle resume logic
        if skipping:
            if chapter_name == resume_from or resume_from in chapter_name:
                skipping = False
            else:
                print(f"\nSkipping {chapter_name} (resuming from {resume_from})")
                continue
        
        # Skip already processed chapters
        if chapter_name in state.processed_chapters:
            print(f"\nSkipping {chapter_name} (already processed)")
            continue
        
        print(f"\n{'='*60}")
        print(f"PROCESSING: {chapter_name}")
        print(f"{'='*60}")
        
        try:
            # Process chapter
            result = process_single_chapter(
                chapter_file=chapter_file,
                arch_spec=arch_spec,
                state=state,
                client=client,
                output_dir=output_dir,
                model=model,
                thinking_budget=thinking_budget
            )
            
            # Update state
            if "state_updates" in result:
                state.apply_updates(result["state_updates"])
            
            state.processed_chapters.append(chapter_name)
            state.last_updated = datetime.now().isoformat()
            
            # Generate code files
            if "articles" in result and result["articles"]:
                print(f"\n  Generating {len(result['articles'])} module stubs...")
                generated = generate_module_files(
                    articles=result["articles"],
                    output_dir=output_dir / "maxwell"
                )
                state.generated_files.extend(generated)
                print(f"    Generated {len(generated)} files")
            
            # Save chapter result
            result_file = output_dir / "results" / f"{chapter_name}_result.json"
            result_file.parent.mkdir(parents=True, exist_ok=True)
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
            
            # Save checkpoint
            state.save(state_file)
            print(f"\n  ✓ Checkpoint saved")
            
            print(f"\n  COMPLETED: {chapter_name}")
            print(f"    Articles processed: {len(result.get('articles', []))}")
            
        except Exception as e:
            print(f"\n  ERROR processing {chapter_name}: {e}")
            import traceback
            traceback.print_exc()
            
            # Save partial state
            state.save(state_file)
            print(f"  State saved. Resume with --resume {chapter_name}")
            sys.exit(1)
    
    # Final summary
    print(f"\n{'='*60}")
    print("PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"  Chapters processed: {len(state.processed_chapters)}")
    print(f"  Modules registered: {len(state.module_registry)}")
    print(f"  Files generated: {len(state.generated_files)}")
    print(f"\nOutput directory: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Process Maxwell's Treatise OCR JSON files into Python modules"
    )
    
    parser.add_argument(
        "--part", "-p",
        type=Path,
        required=True,
        help="Directory containing CHAPTER_*.JSON files"
    )
    
    parser.add_argument(
        "--arch", "-a",
        type=Path,
        default=Path("specs/Part_I_Architecture.md"),
        help="Path to architecture specification markdown"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path("output"),
        help="Output directory for generated code"
    )
    
    parser.add_argument(
        "--model", "-m",
        type=str,
        default="anthropic/claude-sonnet-4-20250514",
        help="OpenRouter model identifier"
    )
    
    parser.add_argument(
        "--thinking-budget", "-t",
        type=int,
        default=10000,
        help="Token budget for extended thinking"
    )
    
    parser.add_argument(
        "--resume", "-r",
        type=str,
        default=None,
        help="Resume from a specific chapter (e.g., CHAPTER_III)"
    )
    
    parser.add_argument(
        "--api-key", "-k",
        type=str,
        default=None,
        help="OpenRouter API key (or set OPENROUTER_API_KEY env)"
    )
    
    args = parser.parse_args()
    
    process_treatise(
        part_dir=args.part,
        arch_path=args.arch,
        output_dir=args.output,
        model=args.model,
        thinking_budget=args.thinking_budget,
        resume_from=args.resume,
        api_key=args.api_key
    )


if __name__ == "__main__":
    main()
