# 🔐 File Integrity Checker

A lightweight Bash + Python tool to verify the integrity of application log files using SHA-256 hashes. This can help detect unauthorized tampering or corruption in logs — an essential step in hardening system security.

---

## 📌 Features

- ✅ Accepts a directory or a single file as input
- 🔐 Uses **SHA-256** cryptographic hash for verification
- 📁 Stores baseline hashes securely in `hashes.json`
- 📊 Compares current file hashes with stored ones to detect changes
- 🔄 Allows manual re-initialization and update of baseline hashes

---

## 🛠️ Requirements

- Python 3.x
- Bash (Unix-like environment)
- sudo permissions (to access system log files if needed)

---

## 🚀 Usage

Clone this repo and make the script executable:

```bash
chmod +x integrity-check
🏁 Initialize Hashes
bash
Copy
Edit
sudo ./integrity-check init /var/log/myapp.log
First-time setup: stores the current hash(s) for the file(s).

🔍 Check File Integrity
bash
Copy
Edit
sudo ./integrity-check check /var/log/myapp.log
Output:

✅ Unmodified: hash matches baseline

⚠️ Modified: file was tampered

🆕 New file: no baseline exists

🔄 Update Hash
bash
Copy
Edit
sudo ./integrity-check update /var/log/myapp.log
Use after you’ve verified the changes and want to set a new baseline.

📁 Example
bash
Copy
Edit
# Create a dummy log file
sudo touch /var/log/myapp.log
echo "Log entry: $(date)" | sudo tee -a /var/log/myapp.log

# Initialize hash
sudo ./integrity-check init /var/log/myapp.log

# Tamper it
echo "UNAUTHORIZED CHANGE" | sudo tee -a /var/log/myapp.log

# Check integrity
sudo ./integrity-check check /var/log/myapp.log

This is the project link: https://roadmap.sh/projects/file-integrity-checker
