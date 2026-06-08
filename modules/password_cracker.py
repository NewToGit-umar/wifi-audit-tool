import subprocess
import os
import re
import time
from pathlib import Path

class PasswordCracker:
    def __init__(self, cap_file, wordlist):
        self.cap_file = cap_file
        self.wordlist = wordlist
        self.process = None
        self.found_password = None

    def crack_password(self):
        if not os.path.exists(self.wordlist):
            yield f"[!] Error: Wordlist '{self.wordlist}' not found"
            return
        if not os.path.exists(self.cap_file):
            yield f"[!] Error: Capture file '{self.cap_file}' not found"
            return

        yield f"[*] Starting aircrack-ng on {os.path.basename(self.cap_file)}"
        yield f"[*] Wordlist: {os.path.basename(self.wordlist)}"
        yield "[*] Cracking... (this can take time)"

        try:
            cmd = ["aircrack-ng", "-w", self.wordlist, self.cap_file]
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            for line in self.process.stdout:
                line = line.strip()
                if line:
                    yield line
                    if "KEY FOUND" in line:
                        match = re.search(r"\[(.+?)\]", line)
                        if match:
                            self.found_password = match.group(1)
                            yield f"\n[+] SUCCESS! PASSWORD: {self.found_password}"
                            break

            if self.process.returncode != 0:
                stderr = self.process.stderr.read()
                if stderr:
                    yield f"[!] Error: {stderr.strip()}"
        except FileNotFoundError:
            yield "[!] aircrack-ng not found. Install with: sudo apt install aircrack-ng"
        except Exception as e:
            yield f"[!] Exception: {str(e)}"

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()