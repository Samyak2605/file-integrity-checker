# File Integrity Checker

This tool detects log file tampering by storing and comparing cryptographic hashes (SHA-256).

## Features

- Supports individual files or entire directories
- Stores and compares SHA-256 hashes
- Reports modified or new files
- Allows manual hash update

## Usage

```bash
# Initialize
./integrity-check init /var/log

# Check
./integrity-check check /var/log/syslog

# Update
./integrity-check update /var/log/syslog


This is the project link: https://roadmap.sh/projects/file-integrity-checker
