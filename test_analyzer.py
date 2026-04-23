#!/usr/bin/env python3
"""Test the FolderAnalyzer on some real folders"""

from pathlib import Path
from personal_data_organizer.analyzers import FolderAnalyzer

# Test folders
test_folders = [
    "~/hack",
    "~/personal-data-organizer",
    "~/courses",
    "~/kubernetes",
]

print("=" * 80)
print("FOLDER ANALYSIS TEST")
print("=" * 80)

for folder_path in test_folders:
    path = Path(folder_path).expanduser()
    
    if not path.exists():
        print(f"\n❌ {folder_path} - Does not exist")
        continue
    
    print(f"\n📁 Analyzing: {folder_path}")
    print("-" * 80)
    
    try:
        analyzer = FolderAnalyzer(path)
        result = analyzer.analyze()
        
        print(f"Size: {result.size / 1024 / 1024:.2f} MB")
        print(f"Files: {result.file_count}")
        print(f"Empty: {result.is_empty}")
        print(f"Git repo: {result.is_git_repo}")
        
        if result.is_git_repo:
            print(f"  - Remote: {result.remote_url}")
            print(f"  - Uncommitted changes: {result.has_uncommitted_changes}")
            print(f"  - Unpushed commits: {result.has_unpushed_commits}")
        
        print(f"Has node_modules: {result.has_node_modules}")
        print(f"Has venv: {result.has_venv}")
        print(f"Has __pycache__: {result.has_pycache}")
        print(f"Has README: {result.has_readme}")
        
        print(f"\n🎯 RECOMMENDATION: {result.recommendations.value}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 80)
