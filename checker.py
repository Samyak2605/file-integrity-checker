import os
import hashlib
import json
import sys

HASH_STORE = "hashes.json"

def compute_file_hash(path):
    sha256 = hashlib.sha256()
    path = os.path.realpath(path)  # Normalize symlinks and relative paths
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"❌ Error reading {path}: {e}")
        return None

def load_hashes():
    if os.path.exists(HASH_STORE):
        with open(HASH_STORE, 'r') as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    with open(HASH_STORE, 'w') as f:
        json.dump(hashes, f, indent=2)

def hash_all_logs(target):
    files = []
    target = os.path.realpath(target)

    if os.path.isdir(target):
        for root, _, filenames in os.walk(target):
            for name in filenames:
                files.append(os.path.join(root, name))
    elif os.path.isfile(target):
        files.append(target)
    else:
        print(f"❌ {target} is not valid.")
        return {}

    result = {}
    for path in files:
        full_path = os.path.realpath(path)
        file_hash = compute_file_hash(full_path)
        if file_hash:
            result[full_path] = file_hash
        else:
            print(f"⚠️ Skipping unreadable file: {full_path}")

    return result

def init(target):
    hashes = hash_all_logs(target)
    if hashes:
        save_hashes(hashes)
        print("✅ Hashes stored successfully.")
    else:
        print("❌ No valid files to hash.")

def check(target):
    old_hashes = load_hashes()
    if not old_hashes:
        print("❌ No stored hashes found. Run 'init' first.")
        return

    if os.path.isdir(target):
        files = [os.path.join(root, name)
                 for root, _, filenames in os.walk(target)
                 for name in filenames]
    elif os.path.isfile(target):
        files = [target]
    else:
        print(f"❌ {target} is not valid.")
        return

    for f in files:
        real_f = os.path.realpath(f)
        current_hash = compute_file_hash(real_f)
        if not current_hash:
            continue
        if real_f in old_hashes:
            if current_hash != old_hashes[real_f]:
                print(f"⚠️ {real_f}: Modified (Hash mismatch)")
            else:
                print(f"✅ {real_f}: Unmodified")
        else:
            print(f"🆕 {real_f}: New file (no baseline hash)")

def update(target):
    hashes = load_hashes()
    if hashes is None:
        print("❌ Failed to load hashes.")
        return

    updated = hash_all_logs(target)
    if updated:
        hashes.update(updated)
        save_hashes(hashes)
        print("🔄 Hash updated successfully.")
    else:
        print("❌ No valid files to update.")

def main():
    if len(sys.argv) < 3:
        print("Usage: ./integrity-check [init|check|update] <file|directory>")
        return

    command = sys.argv[1]
    target = sys.argv[2]

    if command == "init":
        init(target)
    elif command == "check":
        check(target)
    elif command == "update":
        update(target)
    else:
        print("❌ Invalid command. Use init, check, or update.")

if __name__ == "__main__":
    main()
