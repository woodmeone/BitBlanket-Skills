#!/usr/bin/env python3
import sys
import os
import re
import yaml
import zipfile
from pathlib import Path
from datetime import datetime

def validate_skill(skill_path):
    skill_path = Path(skill_path)
    skill_md = skill_path / 'SKILL.md'
    
    if not skill_md.exists():
        return False, "SKILL.md not found"
    
    content = skill_md.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"
    
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"
    
    frontmatter_text = match.group(1)
    
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"
    
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"
    
    name = frontmatter.get('name', '')
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, f"Name '{name}' should be kebab-case"
    
    return True, "Skill is valid!"

def package_skill(skill_path, output_dir=None):
    skill_path = Path(skill_path)
    if output_dir is None:
        output_dir = skill_path.parent
    else:
        output_dir = Path(output_dir)
    
    valid, message = validate_skill(skill_path)
    if not valid:
        return False, message
    
    skill_md = skill_path / 'SKILL.md'
    content = skill_md.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    frontmatter = yaml.safe_load(match.group(1))
    name = frontmatter.get('name', skill_path.name)
    
    output_file = output_dir / f"{name}.skill"
    
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in skill_path.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(skill_path)
                zf.write(file_path, arcname)
    
    return True, str(output_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python package.py <skill_directory> [output_directory]")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"Packaging skill: {skill_path}")
    
    valid, msg = validate_skill(skill_path)
    if not valid:
        print(f"Validation failed: {msg}")
        sys.exit(1)
    
    print("Validation passed!")
    
    success, result = package_skill(skill_path, output_dir)
    if success:
        print(f"Package created: {result}")
    else:
        print(f"Packaging failed: {result}")
        sys.exit(1)
