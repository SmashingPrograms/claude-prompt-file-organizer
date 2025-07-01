# Claude Prompt File Organizer

This is a script that will put together all your local files in a certain folder into a text file, to use for your Claude prompt that can read your entire codebase at once.

## How It Works

This script is written in Python. Whatever the current folder is, it will collect every file's data within it. Example:

```
./coding-practice
./coding-practice/README.md
./coding-practice/scripts
./coding-practice/scripts/do.py
```

If you enter `prompt-get`, it will create a text file called `prompt.txt` in the folder you're currently in in your terminal (assuming you're in coding-practice).

It will consolidate all of the content in all folders and subfolders as follows:

```
# ./coding-practice/README.md

Hi. This is a README.

# ./coding-practice/scripts/do.py

print("Hi")
if True:
    print("It's true")
```

## Rules

- If it ends in `.py`, it will put a `#` comment at the beginning to say the filename
- If it ends in `.js`, `.jsx`, `.ts`, or `.tsx`, it will put `//` at the beginning
- If it's a `.html` or `.css` file, it will put a `<!-- -->` comment at the beginning
- **Automatically skips**: `.git` directories, `node_modules` folders, `__pycache__` folders, `venv` folders, `package.json`, `package-lock.json`, hidden files (starting with `.`), and the output file itself

## How to Make It Usable

```bash
sudo ln -s /Users/bobbybumps/supercode/claude-prompt-file-organizer/prompt_get.py /usr/local/bin/prompt-get
```

## Usage

After setting up the global command, simply run:

```bash
prompt-get
```

This will generate a `prompt.txt` file in your current directory with all files consolidated.

## Testing

Run the automated test suite:

```bash
prompt-get --test
```

The test suite includes three comprehensive tests:

### Test 1: Comment Header Generation
Tests that the correct comment style is applied for different file types:
- **Python files** (`.py`) → `# filename.py`
- **JavaScript/TypeScript files** (`.js`, `.jsx`, `.ts`, `.tsx`) → `// filename.js`
- **HTML/CSS files** (`.html`, `.css`) → `<!-- filename.html -->`
- **Other files** (`.md`, etc.) → `# filename.md`

### Test 2: File Skip Logic
Verifies that the script correctly skips unwanted files:
- **Hidden files** (`.gitignore`, `.DS_Store`) → Skipped ✓
- **Output file** (`prompt.txt`) → Skipped ✓
- **Package files** (`package.json`, `package-lock.json`) → Skipped ✓
- **Files in `node_modules`** (`node_modules/package.json`) → Skipped ✓
- **Files in `__pycache__`** (`src/__pycache__/module.pyc`) → Skipped ✓
- **Files in `venv`** (`venv/bin/python`) → Skipped ✓
- **Normal files** (`normal.py`, `src/components/App.jsx`) → Included ✓

### Test 3: Integration Test
Creates a temporary directory with test files and runs the full consolidation process:
- Creates test files: `test.py`, `script.js`, `style.css`, `index.html`, `.gitignore`, `package.json`, `package-lock.json`
- Creates skip directories: `node_modules`, `__pycache__`, `venv` (with test files inside)
- Runs the consolidation process
- Verifies that `prompt.txt` is created with the correct content
- Ensures hidden files (`.gitignore`), package files, and skip directories are properly excluded
- Validates that all expected files are included with proper comment headers