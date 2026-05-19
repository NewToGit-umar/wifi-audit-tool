# W1F1_Pwn (Auto-Hack Tool)

W1F1_Pwn is an automated Wi-Fi security auditing and pentesting suite with a custom matrix-themed Graphical User Interface (GUI). 
It streamlines the process of capturing WPA/WPA2 handshakes automatically using standard tools like \ircrack-ng\ and \ireplay-ng\. It also includes the built-in \CUPP\ module to automatically generate hyper-customized target-specific wordlists via interactive prompts to increase password cracking success rates.

### Features
- Native Python/PyQt5 automated Cyber GUI
- 1-Click Handshake Auto-Pwn workflows
- Integrated Custom Wordlist Generator
- Cross-platform network scanning natively wired to \
mcli\
- Interactive Wordlist launching terminals

### How to Install and Run
Installing and running this tool is completely automated. You do not need to manually configure permissions or download python modules.

1. Clone the repository into your desired folder:
   \\\ash
   git clone https://github.com/NewToGit-umar/wifi-audit-tool.git
   cd wifi-audit-tool
   \\\

2. Run the tool initialization script:
   \\\ash
   sudo bash wifi-audit-tool
   \\\
   *(Note: The very first time you run this, it will automatically install ircrack-ng, dependency packages, link 
ockyou.txt, and configure itself. The app will open immediately after).*

3. **Global Execution:**
   After running it for the first time, a global system shortcut is created automatically. From then on, you can open any terminal from anywhere on your system and launch the suite by simply typing:
   \\\ash
   sudo wifi-audit-tool
   \\\

### Requirements
- Kali Linux / Parrot Security / Ubuntu
- Root (sudo) privileges
- Wi-Fi Adapter with Monitor Mode and Packet Injection support (for capture mode)
