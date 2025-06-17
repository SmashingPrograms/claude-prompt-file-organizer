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