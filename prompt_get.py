#!/usr/bin/env python3
"""
Prompt File Organizer - Consolidates all files in current directory into prompt.txt
for use with Claude prompts that can read entire codebases at once.
"""

import os
import sys
from pathlib import Path
import argparse


def get_comment_header(file_path):
    """
    Get the appropriate comment header based on file extension.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Comment header for the file
    """
    print(f"Determining comment header for: {file_path}")
    
    file_ext = Path(file_path).suffix.lower()
    
    if file_ext == '.py':
        print(f"  - Python file detected (.py), using # comment style")
        return f"# {file_path}\n"
    elif file_ext in ['.js', '.jsx', '.ts', '.tsx']:
        print(f"  - JavaScript/TypeScript file detected ({file_ext}), using // comment style")
        return f"// {file_path}\n"
    elif file_ext in ['.html', '.css']:
        print(f"  - HTML/CSS file detected ({file_ext}), using <!-- --> comment style")
        return f"<!-- {file_path} -->\n"
    else:
        print(f"  - Other file type detected ({file_ext}), using # comment style")
        return f"# {file_path}\n"


def should_skip_file(file_path):
    """
    Determine if a file should be skipped (hidden files, directories, etc.).
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        bool: True if file should be skipped, False otherwise
    """
    path = Path(file_path)
    
    # Skip hidden files and directories
    if path.name.startswith('.'):
        print(f"  - Skipping hidden file/directory: {file_path}")
        return True
    
    # Skip directories
    if path.is_dir():
        print(f"  - Skipping directory: {file_path}")
        return True
    
    # Skip the output file itself
    if path.name == 'prompt.txt':
        print(f"  - Skipping output file: {file_path}")
        return True
    
    # Skip package.json and package-lock.json files
    if path.name in ['package.json', 'package-lock.json']:
        print(f"  - Skipping package file: {file_path}")
        return True
    
    # Skip files in node_modules, __pycache__, and venv directories
    path_parts = path.parts
    for part in path_parts:
        if part in ['node_modules', '__pycache__', 'venv']:
            print(f"  - Skipping file in {part} directory: {file_path}")
            return True
    
    return False


def read_file_content(file_path):
    """
    Read the content of a file with error handling.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: File content or error message
    """
    try:
        print(f"  - Reading file content...")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"  - Successfully read {len(content)} characters")
        return content
    except UnicodeDecodeError:
        print(f"  - Error: File contains non-text content, skipping")
        return f"[BINARY FILE - {file_path}]\n"
    except Exception as e:
        print(f"  - Error reading file: {e}")
        return f"[ERROR READING FILE - {file_path}: {e}]\n"


def consolidate_files(current_dir):
    """
    Consolidate all files in the current directory and subdirectories into prompt.txt.
    
    Args:
        current_dir (str): Current working directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"Starting file consolidation in directory: {current_dir}")
    
    output_file = os.path.join(current_dir, 'prompt.txt')
    consolidated_content = []
    
    # Walk through all files and subdirectories
    print("Scanning directory structure...")
    for root, dirs, files in os.walk(current_dir):
        # Skip .git directory entirely
        if '.git' in dirs:
            print(f"  - Skipping .git directory in: {root}")
            dirs.remove('.git')
        
        # Skip node_modules, __pycache__, and venv directories entirely
        for skip_dir in ['node_modules', '__pycache__', 'venv']:
            if skip_dir in dirs:
                print(f"  - Skipping {skip_dir} directory in: {root}")
                dirs.remove(skip_dir)
        
        print(f"  - Scanning directory: {root}")
        
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, current_dir)
            
            print(f"  - Processing file: {relative_path}")
            
            if should_skip_file(relative_path):
                continue
            
            # Get appropriate comment header
            comment_header = get_comment_header(relative_path)
            
            # Read file content
            file_content = read_file_content(file_path)
            
            # Add to consolidated content
            consolidated_content.append(comment_header)
            consolidated_content.append(file_content)
            consolidated_content.append("\n\n")
            
            print(f"  - Added file to consolidation")
    
    # Write consolidated content to prompt.txt
    print(f"Writing consolidated content to: {output_file}")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(consolidated_content)
        
        total_files = len([item for item in consolidated_content if item.startswith('#') or item.startswith('//') or item.startswith('<!--')])
        print(f"Successfully created {output_file} with {total_files} files consolidated")
        return True
        
    except Exception as e:
        print(f"Error writing output file: {e}")
        return False


def main():
    """
    Main function to run the prompt file organizer.
    """
    parser = argparse.ArgumentParser(description='Consolidate all files in current directory into prompt.txt')
    parser.add_argument('--test', action='store_true', help='Run automated tests')
    args = parser.parse_args()
    
    if args.test:
        print("Running automated tests...")
        run_tests()
        return
    
    print("=== Prompt File Organizer ===")
    print("This script will consolidate all files in the current directory into prompt.txt")
    print("for use with Claude prompts that can read entire codebases at once.\n")
    
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")
    
    success = consolidate_files(current_dir)
    
    if success:
        print("\n=== Consolidation Complete ===")
        print("Your prompt.txt file has been created successfully!")
        print("You can now use this file with Claude to provide context about your codebase.")
    else:
        print("\n=== Consolidation Failed ===")
        print("There was an error during the consolidation process.")
        sys.exit(1)


def run_tests():
    """
    Run automated tests to verify functionality.
    """
    print("=== Running Automated Tests ===")
    
    # Test 1: Comment header generation
    print("\nTest 1: Comment header generation")
    test_comment_headers()
    
    # Test 2: File skip logic
    print("\nTest 2: File skip logic")
    test_file_skip_logic()
    
    # Test 3: Integration test
    print("\nTest 3: Integration test")
    test_integration()
    
    print("\n=== All Tests Complete ===")


def test_comment_headers():
    """Test comment header generation for different file types."""
    test_cases = [
        ('test.py', '# test.py\n'),
        ('script.js', '// script.js\n'),
        ('component.tsx', '// component.tsx\n'),
        ('style.css', '<!-- style.css -->\n'),
        ('index.html', '<!-- index.html -->\n'),
        ('README.md', '# README.md\n'),
    ]
    
    for file_path, expected in test_cases:
        result = get_comment_header(file_path)
        if result == expected:
            print(f"  ✓ {file_path}: PASS")
        else:
            print(f"  ✗ {file_path}: FAIL (expected '{expected}', got '{result}')")


def test_file_skip_logic():
    """Test file skip logic."""
    test_cases = [
        ('.gitignore', True),  # Hidden file
        ('.DS_Store', True),   # Hidden file
        ('normal.py', False),  # Normal file
        ('prompt.txt', True),  # Output file
        ('package.json', True),  # Package file
        ('package-lock.json', True),  # Package lock file
        ('node_modules/package.json', True),  # File in node_modules
        ('src/__pycache__/module.pyc', True),  # File in __pycache__
        ('venv/bin/python', True),  # File in venv
        ('src/components/App.jsx', False),  # Normal file in subdirectory
    ]
    
    for file_path, expected in test_cases:
        result = should_skip_file(file_path)
        if result == expected:
            print(f"  ✓ {file_path}: PASS")
        else:
            print(f"  ✗ {file_path}: FAIL (expected {expected}, got {result})")


def test_integration():
    """Test integration by creating a temporary directory with test files."""
    import tempfile
    import shutil
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"  - Created temporary directory: {temp_dir}")
        
        # Create test files
        test_files = {
            'test.py': 'print("Hello World")',
            'script.js': 'console.log("Hello World")',
            'style.css': 'body { color: red; }',
            'index.html': '<html><body>Hello</body></html>',
            '.gitignore': '*.pyc',  # Should be skipped
            'package.json': '{"name": "test"}',  # Should be skipped
            'package-lock.json': '{"lockfileVersion": 1}',  # Should be skipped
        }
        
        # Create directories that should be skipped
        skip_dirs = ['node_modules', '__pycache__', 'venv']
        for skip_dir in skip_dirs:
            skip_dir_path = os.path.join(temp_dir, skip_dir)
            os.makedirs(skip_dir_path, exist_ok=True)
            # Add a file in each skip directory
            skip_file_path = os.path.join(skip_dir_path, f'test_{skip_dir}.txt')
            with open(skip_file_path, 'w') as f:
                f.write(f'This file in {skip_dir} should be skipped')
            print(f"  - Created skip directory: {skip_dir}")
        
        for filename, content in test_files.items():
            file_path = os.path.join(temp_dir, filename)
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"  - Created test file: {filename}")
        
        # Run consolidation
        success = consolidate_files(temp_dir)
        
        if success:
            # Check if prompt.txt was created
            output_file = os.path.join(temp_dir, 'prompt.txt')
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    content = f.read()
                
                # Verify content contains expected files
                expected_files = ['test.py', 'script.js', 'style.css', 'index.html']
                missing_files = [f for f in expected_files if f not in content]
                
                # Verify skip directories are not included
                skip_files = ['test_node_modules.txt', 'test___pycache__.txt', 'test_venv.txt']
                included_skip_files = [f for f in skip_files if f in content]
                
                # Verify package files are not included
                package_files = ['package.json', 'package-lock.json']
                included_package_files = [f for f in package_files if f in content]
                
                if not missing_files and '.gitignore' not in content and not included_skip_files and not included_package_files:
                    print("  ✓ Integration test: PASS")
                else:
                    print(f"  ✗ Integration test: FAIL (missing: {missing_files}, included skip files: {included_skip_files}, included package files: {included_package_files})")
            else:
                print("  ✗ Integration test: FAIL (prompt.txt not created)")
        else:
            print("  ✗ Integration test: FAIL (consolidation failed)")


if __name__ == "__main__":
    main() 