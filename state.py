"""
State Management for Maxwell Treatise Processing

This module maintains processing state across chapters to:
1. Track which chapters have been processed
2. Maintain module/class/function registries
3. Track cross-references between articles
4. Enable resume from checkpoints
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path
import json
from datetime import datetime


@dataclass
class ProcessingState:
    """
    Persistent state object that tracks progress across chapter processing.
    
    This state is:
    - Serializable to JSON for checkpointing
    - Compact enough to include in prompts (~1000-2000 tokens when summarized)
    - Complete enough to provide context for subsequent chapters
    """
    
    # Identity
    part: str = ""                              # e.g., "PART_I_ELECTROSTATICS"
    volume: int = 1                             # 1 or 2
    
    # Progress tracking
    processed_chapters: List[str] = field(default_factory=list)
    last_updated: str = ""
    
    # Module registry: maps module paths to article numbers
    # e.g., {"maxwell/core/charge.py": ["27", "28", "29", "30"]}
    module_registry: Dict[str, List[str]] = field(default_factory=dict)
    
    # Class registry: maps class names to their module paths
    # e.g., {"ElectrifiedBody": "maxwell/core/charge.py"}
    class_registry: Dict[str, str] = field(default_factory=dict)
    
    # Function registry: maps function names to their module paths
    # e.g., {"coulomb_law": "maxwell/physics/forces.py"}
    function_registry: Dict[str, str] = field(default_factory=dict)
    
    # Cross-references discovered in the text
    # e.g., {"27": ["100c"], "85a": ["84"]}
    forward_refs: Dict[str, List[str]] = field(default_factory=dict)
    backward_refs: Dict[str, List[str]] = field(default_factory=dict)
    
    # Equations extracted (article → list of LaTeX equations)
    equations: Dict[str, List[str]] = field(default_factory=dict)
    
    # Generated file paths
    generated_files: List[str] = field(default_factory=list)
    
    # Metadata
    total_articles_processed: int = 0
    
    def to_summary_string(self) -> str:
        """
        Generate a COMPACT summary for inclusion in prompts.
        
        This summary tells the AI what has already been done without
        including the full content of previous chapters.
        """
        lines = [
            f"=== PROCESSING STATE SUMMARY ===",
            f"Part: {self.part}",
            f"Volume: {self.volume}",
            f"Chapters Processed: {', '.join(self.processed_chapters) or 'None'}",
            f"Total Articles: {self.total_articles_processed}",
            "",
            "--- Modules Created ---"
        ]
        
        for module, articles in sorted(self.module_registry.items()):
            lines.append(f"  {module}: Arts. {', '.join(articles[:5])}" + 
                        (f"... (+{len(articles)-5} more)" if len(articles) > 5 else ""))
        
        if self.class_registry:
            lines.append("")
            lines.append("--- Classes Defined ---")
            for cls, module in sorted(self.class_registry.items())[:20]:
                lines.append(f"  {cls} → {module}")
            if len(self.class_registry) > 20:
                lines.append(f"  ... and {len(self.class_registry) - 20} more")
        
        if self.function_registry:
            lines.append("")
            lines.append("--- Functions Defined ---")
            for func, module in sorted(self.function_registry.items())[:20]:
                lines.append(f"  {func}() → {module}")
            if len(self.function_registry) > 20:
                lines.append(f"  ... and {len(self.function_registry) - 20} more")
        
        if self.forward_refs:
            lines.append("")
            lines.append("--- Cross-References Noted ---")
            ref_count = sum(len(refs) for refs in self.forward_refs.values())
            lines.append(f"  {ref_count} forward references across {len(self.forward_refs)} articles")
        
        lines.append("")
        lines.append("=== END STATE SUMMARY ===")
        
        return "\n".join(lines)
    
    def to_dict(self) -> dict:
        """Convert state to dictionary for JSON serialization."""
        return {
            "part": self.part,
            "volume": self.volume,
            "processed_chapters": self.processed_chapters,
            "last_updated": self.last_updated,
            "module_registry": self.module_registry,
            "class_registry": self.class_registry,
            "function_registry": self.function_registry,
            "forward_refs": self.forward_refs,
            "backward_refs": self.backward_refs,
            "equations": self.equations,
            "generated_files": self.generated_files,
            "total_articles_processed": self.total_articles_processed
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProcessingState":
        """Create state from dictionary (JSON deserialization)."""
        return cls(
            part=data.get("part", ""),
            volume=data.get("volume", 1),
            processed_chapters=data.get("processed_chapters", []),
            last_updated=data.get("last_updated", ""),
            module_registry=data.get("module_registry", {}),
            class_registry=data.get("class_registry", {}),
            function_registry=data.get("function_registry", {}),
            forward_refs=data.get("forward_refs", {}),
            backward_refs=data.get("backward_refs", {}),
            equations=data.get("equations", {}),
            generated_files=data.get("generated_files", []),
            total_articles_processed=data.get("total_articles_processed", 0)
        )
    
    def save(self, path: Path):
        """Save state to JSON file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, path: Path) -> "ProcessingState":
        """Load state from JSON file."""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def apply_updates(self, updates: dict):
        """
        Apply state updates from a chapter processing result.
        
        Expected updates format:
        {
            "new_modules": {"path": ["articles"]},
            "new_classes": {"ClassName": "module_path"},
            "new_functions": {"func_name": "module_path"},
            "forward_refs": {"art": ["refs"]},
            "backward_refs": {"art": ["refs"]},
            "equations": {"art": ["latex"]}
        }
        """
        if "new_modules" in updates:
            for module, articles in updates["new_modules"].items():
                if module not in self.module_registry:
                    self.module_registry[module] = []
                self.module_registry[module].extend(articles)
                # Deduplicate
                self.module_registry[module] = list(set(self.module_registry[module]))
        
        if "new_classes" in updates:
            self.class_registry.update(updates["new_classes"])
        
        if "new_functions" in updates:
            self.function_registry.update(updates["new_functions"])
        
        if "forward_refs" in updates:
            for art, refs in updates["forward_refs"].items():
                if art not in self.forward_refs:
                    self.forward_refs[art] = []
                self.forward_refs[art].extend(refs)
        
        if "backward_refs" in updates:
            for art, refs in updates["backward_refs"].items():
                if art not in self.backward_refs:
                    self.backward_refs[art] = []
                self.backward_refs[art].extend(refs)
        
        if "equations" in updates:
            self.equations.update(updates["equations"])
        
        if "articles_count" in updates:
            self.total_articles_processed += updates["articles_count"]
    
    def get_article_module(self, article_num: str) -> Optional[str]:
        """Find which module an article is mapped to."""
        for module, articles in self.module_registry.items():
            if article_num in articles:
                return module
        return None
    
    def get_class_module(self, class_name: str) -> Optional[str]:
        """Find which module a class is defined in."""
        return self.class_registry.get(class_name)
    
    def get_function_module(self, func_name: str) -> Optional[str]:
        """Find which module a function is defined in."""
        return self.function_registry.get(func_name)


# Convenience functions

def create_fresh_state(part_name: str, volume: int = 1) -> ProcessingState:
    """Create a new processing state for a Part."""
    return ProcessingState(
        part=part_name,
        volume=volume,
        last_updated=datetime.now().isoformat()
    )


def load_or_create_state(
    state_file: Path, 
    part_name: str, 
    volume: int = 1
) -> ProcessingState:
    """Load existing state or create new one."""
    if state_file.exists():
        return ProcessingState.load(state_file)
    return create_fresh_state(part_name, volume)
