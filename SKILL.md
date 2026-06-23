# generate-changelog

Generate a structured CHANGELOG.md from git history.

## Usage
```
/generate-changelog
```
Or run standalone: `bash changelog.sh`

## How it works
1. Fetches commits since the last git tag
2. Auto-categorizes into: Added / Fixed / Changed / Removed
3. Outputs CHANGELOG.md

## Requirements
- git installed
- bash
