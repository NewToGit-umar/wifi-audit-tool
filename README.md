# W1F1_Pwn (Auto-Hack Tool)

W1F1_Pwn is an automated Wi-Fi security auditing and penetration testing suite with a custom matrix-themed Graphical User Interface (GUI).

It streamlines the process of capturing WPA/WPA2 handshakes automatically using standard tools like `aircrack-ng` and `aireplay-ng`. It also includes a built-in `CUPP` module to automatically generate highly customized, target-specific wordlists through interactive prompts, increasing password cracking success rates.

## Features

- Native Python/PyQt5 automated cyber GUI
- One-click handshake auto-capture workflows
- Integrated custom wordlist generator
- Cross-platform network scanning integrated with `nmcli`
- Interactive terminal-based wordlist launching

## How to Install and Run

Installing and running this tool is fully automated. You do not need to manually configure permissions or install Python modules.

### 1. Clone the Repository

```bash
git clone https://github.com/NewToGit-umar/wifi-audit-tool.git
cd wifi-audit-tool
```

### 2. Run the Initialization Script

```bash
sudo bash wifi-audit-tool
```

> **Note:**  
> The first time you run the tool, it will automatically install `aircrack-ng`, required dependency packages, configure itself, and create the necessary symlinks (including `rockyou.txt`). The application will launch automatically after setup.

### 3. Global Execution

After the first run, a global system shortcut is created automatically. You can then launch the suite from any terminal using:

```bash
sudo wifi-audit-tool
```

## Requirements

- Kali Linux
- Parrot Security OS
- Ubuntu
- Root (`sudo`) privileges
- Wi-Fi adapter with Monitor Mode and Packet Injection support (required for capture mode)

## Disclaimer

This tool is intended strictly for authorized security auditing, educational purposes, and penetration testing in environments where you have explicit permission. Unauthorized access to networks is illegal and unethical.
