"""
Code Generator for Maxwell Treatise Python Library

This module takes the processed article results and generates
actual Python module files with proper structure.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


# File header template
FILE_HEADER = '''"""
{module_title}

Auto-generated from Maxwell's "A Treatise on Electricity and Magnetism"
Articles: {articles}
Generated: {timestamp}

This module is part of the maxwell package, a modern Python implementation
of Maxwell's electromagnetic theory.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union, List, Tuple
import numpy as np
from numpy.typing import ArrayLike

if TYPE_CHECKING:
    from maxwell.core.fields import ElectricField
    from maxwell.core.charge import Charge

'''


def generate_module_files(
    articles: List[Dict],
    output_dir: Path,
    overwrite: bool = False
) -> List[str]:
    """
    Generate Python module files from processed articles.
    
    Args:
        articles: List of article dictionaries from AI processing
        output_dir: Base directory for maxwell package (e.g., output/maxwell/)
        overwrite: Whether to overwrite existing files
    
    Returns:
        List of generated file paths
    """
    output_dir = Path(output_dir)
    generated_files = []
    
    # Group articles by module
    modules: Dict[str, List[Dict]] = {}
    for article in articles:
        module_path = article.get('module_path', '')
        if not module_path:
            continue
        
        if module_path not in modules:
            modules[module_path] = []
        modules[module_path].append(article)
    
    # Generate each module
    for module_path, module_articles in modules.items():
        file_path = output_dir / module_path
        
        # Check if file exists
        if file_path.exists() and not overwrite:
            # Append to existing file
            generated = append_to_module(file_path, module_articles)
        else:
            # Create new file
            generated = create_module(file_path, module_articles)
        
        if generated:
            generated_files.append(str(file_path))
    
    # Create __init__.py files for packages
    create_init_files(output_dir, modules.keys())
    
    return generated_files


def create_module(file_path: Path, articles: List[Dict]) -> bool:
    """
    Create a new module file with article implementations.
    
    Returns True if successful.
    """
    # Create parent directories
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Extract module info
    article_nums = [a.get('number', '?') + (a.get('sub') or '') for a in articles]
    module_name = file_path.stem
    
    # Derive title from first article or module name
    if articles and articles[0].get('title'):
        module_title = articles[0]['title']
    else:
        module_title = module_name.replace('_', ' ').title()
    
    # Build file content
    content_parts = [
        FILE_HEADER.format(
            module_title=module_title,
            articles=', '.join(article_nums),
            timestamp=datetime.now().isoformat()
        )
    ]
    
    # Add imports based on content
    imports = collect_imports(articles)
    if imports:
        content_parts.append('\n'.join(imports) + '\n\n')
    
    # Add constants/enums if needed
    constants = generate_constants(articles)
    if constants:
        content_parts.append(constants + '\n\n')
    
    # Add each article's implementation
    for article in articles:
        impl = generate_implementation(article)
        if impl:
            content_parts.append(impl + '\n\n')
    
    # Write file
    content = ''.join(content_parts)
    
    try:
        file_path.write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return False


def append_to_module(file_path: Path, articles: List[Dict]) -> bool:
    """
    Append article implementations to an existing module.
    
    Returns True if successful.
    """
    try:
        existing = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return create_module(file_path, articles)
    
    # Find existing article numbers to avoid duplicates
    existing_arts = set()
    import re
    for match in re.finditer(r'Art\.\s*(\d+\s*[a-z]?)', existing):
        existing_arts.add(match.group(1).replace(' ', ''))
    
    # Add only new articles
    new_content = []
    for article in articles:
        art_num = article.get('number', '') + (article.get('sub') or '')
        if art_num not in existing_arts:
            impl = generate_implementation(article)
            if impl:
                new_content.append(impl)
    
    if not new_content:
        return True  # Nothing to add
    
    # Append new content
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write('\n\n# === Additional Articles ===\n\n')
            f.write('\n\n'.join(new_content))
        return True
    except Exception as e:
        print(f"Error appending to {file_path}: {e}")
        return False


def generate_implementation(article: Dict) -> Optional[str]:
    """
    Generate Python code for a single article.
    """
    impl_type = article.get('implementation_type', 'function')
    impl_name = article.get('implementation_name', '')
    stub_code = article.get('stub_code', '')
    
    if not impl_name:
        return None
    
    # If we have stub code from AI, use it
    if stub_code and len(stub_code) > 20:
        # Clean up the stub code
        stub_code = clean_stub_code(stub_code)
        return stub_code
    
    # Otherwise generate minimal stub
    art_num = article.get('number', '?')
    art_sub = article.get('sub') or ''
    title = article.get('title', 'Unknown')
    equations = article.get('equations', [])
    
    if impl_type == 'class':
        return generate_class_stub(impl_name, art_num + art_sub, title, equations)
    elif impl_type == 'function':
        return generate_function_stub(impl_name, art_num + art_sub, title, equations)
    elif impl_type == 'documentation':
        return generate_doc_stub(impl_name, art_num + art_sub, title)
    else:
        return generate_function_stub(impl_name, art_num + art_sub, title, equations)


def generate_class_stub(
    name: str,
    article: str,
    title: str,
    equations: List[str]
) -> str:
    """Generate a class stub."""
    eq_doc = ""
    if equations:
        eq_doc = "\n    \n    Key Equations:\n"
        for eq in equations[:3]:  # Limit to 3 equations
            eq_doc += f"        {eq}\n"
    
    return f'''class {name}:
    """
    Art. {article}: {title}
    
    Maxwell's Treatise on Electricity and Magnetism.{eq_doc}
    """
    
    def __init__(self):
        """Initialize {name}."""
        # TODO: Implement based on Art. {article}
        pass
    
    def __repr__(self) -> str:
        return f"{name}()"
'''


def generate_function_stub(
    name: str,
    article: str,
    title: str,
    equations: List[str]
) -> str:
    """Generate a function stub."""
    eq_doc = ""
    if equations:
        eq_doc = "\n    \n    Key Equations:\n"
        for eq in equations[:3]:
            eq_doc += f"        {eq}\n"
    
    return f'''def {name}(*args, **kwargs):
    """
    Art. {article}: {title}
    
    Maxwell's Treatise on Electricity and Magnetism.{eq_doc}
    
    Args:
        *args: Variable arguments
        **kwargs: Keyword arguments
    
    Returns:
        Implementation pending
    
    Raises:
        NotImplementedError: This function needs implementation
    """
    # TODO: Implement based on Art. {article}
    raise NotImplementedError(f"Art. {article}: {name} not yet implemented")
'''


def generate_doc_stub(name: str, article: str, title: str) -> str:
    """Generate a documentation-only stub (as a constant or comment)."""
    return f'''# Art. {article}: {title}
# 
# This article provides conceptual/theoretical discussion rather than
# computational procedures. See Maxwell's original text for details.
#
{name.upper()}_ARTICLE = "{article}"
{name.upper()}_TITLE = """{title}"""
'''


def clean_stub_code(code: str) -> str:
    """Clean up AI-generated stub code."""
    # Remove markdown code blocks if present
    code = code.strip()
    if code.startswith('```python'):
        code = code[9:]
    elif code.startswith('```'):
        code = code[3:]
    if code.endswith('```'):
        code = code[:-3]
    
    # Ensure proper newlines
    code = code.strip()
    
    # Fix common issues
    code = code.replace('\\n', '\n')  # Escaped newlines
    code = code.replace('\\"', '"')   # Escaped quotes
    
    return code


def collect_imports(articles: List[Dict]) -> List[str]:
    """
    Collect necessary imports based on article content.
    """
    imports = set()
    
    for article in articles:
        code = article.get('stub_code', '')
        
        # Check for numpy usage
        if 'np.' in code or 'numpy' in code.lower():
            imports.add('import numpy as np')
        
        # Check for scipy usage
        if 'scipy' in code.lower():
            imports.add('import scipy')
        
        # Check for dataclass usage
        if '@dataclass' in code:
            imports.add('from dataclasses import dataclass, field')
        
        # Check for enum usage
        if 'Enum' in code:
            imports.add('from enum import Enum, auto')
    
    return sorted(imports)


def generate_constants(articles: List[Dict]) -> str:
    """
    Generate module-level constants if needed.
    """
    constants = []
    
    # Physical constants that might be needed
    has_physics = any('coulomb' in str(a).lower() or 'force' in str(a).lower() 
                      for a in articles)
    
    if has_physics:
        constants.append("""
# Physical Constants (SI units)
EPSILON_0 = 8.8541878128e-12  # Vacuum permittivity (F/m)
K_E = 8.9875517923e9  # Coulomb's constant (N⋅m²/C²)
""")
    
    return '\n'.join(constants)


def create_init_files(output_dir: Path, module_paths: List[str]) -> None:
    """
    Create __init__.py files for all package directories.
    """
    # Collect all unique package paths
    packages = set()
    for module_path in module_paths:
        parts = Path(module_path).parts
        for i in range(len(parts) - 1):  # Exclude the .py file itself
            packages.add(Path(*parts[:i+1]))
    
    # Create __init__.py for each package
    for package in packages:
        init_path = output_dir / package / '__init__.py'
        if not init_path.exists():
            init_path.parent.mkdir(parents=True, exist_ok=True)
            
            package_name = package.parts[-1] if package.parts else 'maxwell'
            content = f'''"""
{package_name} - Maxwell's Treatise Python Implementation

Auto-generated package initialization.
"""

# Package-level imports can be added here
'''
            init_path.write_text(content, encoding='utf-8')


def generate_module_index(output_dir: Path) -> str:
    """
    Generate an index of all modules and their contents.
    """
    lines = ["# Maxwell Package Module Index\n"]
    
    for py_file in sorted(output_dir.rglob("*.py")):
        if py_file.name == "__init__.py":
            continue
        
        rel_path = py_file.relative_to(output_dir)
        lines.append(f"\n## {rel_path}\n")
        
        # Quick parse to find classes and functions
        try:
            content = py_file.read_text(encoding='utf-8')
            
            import re
            classes = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)
            functions = re.findall(r'^def\s+(\w+)', content, re.MULTILINE)
            
            if classes:
                lines.append("Classes: " + ", ".join(classes))
            if functions:
                lines.append("Functions: " + ", ".join(functions))
        except Exception:
            pass
    
    return '\n'.join(lines)


# CLI for testing
if __name__ == "__main__":
    import sys
    import json
    
    if len(sys.argv) < 3:
        print("Usage: python code_generator.py <result.json> <output_dir>")
        sys.exit(1)
    
    result_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    
    with open(result_file, 'r', encoding='utf-8') as f:
        result = json.load(f)
    
    articles = result.get('articles', [])
    print(f"Generating code for {len(articles)} articles...")
    
    generated = generate_module_files(articles, output_dir)
    print(f"Generated {len(generated)} files:")
    for f in generated:
        print(f"  - {f}")
