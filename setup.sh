#!/bin/bash
# Installation script for W1F1_Pwn (Auto-Hack Tool)

echo "W1F1_Pwn (Auto-Hack Tool) Setup"
echo "==============================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (sudo ./setup.sh)"
    exit 1
fi

# Update system
echo "[*] Updating system package list..."
apt-get update

# Install system dependencies (Aircrack-ng suite, networking, PyQt5)
echo "[*] Installing system and Python dependencies..."
apt-get install -y aircrack-ng hashcat hcxtools crunch reaver pixiewps network-manager
apt-get install -y python3-pyqt5 python3-pip git xterm

# Install Python requirements
echo "[*] Installing Python requirements..."
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt

# Create necessary directories
echo "[*] Creating required directories..."
mkdir -p captures wordlists logs

# Setup wordlists
echo "[*] Setting up default wordlists..."
if [ -f "/usr/share/wordlists/rockyou.txt.gz" ]; then
    echo "    Extracting rockyou.txt..."
    gunzip -k /usr/share/wordlists/rockyou.txt.gz 2>/dev/null
    ln -sf /usr/share/wordlists/rockyou.txt wordlists/rockyou.txt
elif [ -f "/usr/share/wordlists/rockyou.txt" ]; then
    ln -sf /usr/share/wordlists/rockyou.txt wordlists/rockyou.txt
else
    echo "    rockyou.txt not found. Using empty/placeholder wordlist."
    touch wordlists/rockyou.txt
fi

# Permissions
chmod +x app.py

# Create a global command wrapper
echo "[*] Creating global command 'wifi-audit-tool'..."
INSTALL_DIR=$(pwd)
cat <<EOF > /usr/local/bin/wifi-audit-tool
#!/bin/bash
if [ "\$EUID" -ne 0 ]; then
  echo "Please run as root (sudo wifi-audit-tool)"
  exit 1
fi
cd "\$INSTALL_DIR"
python3 app.py "\$@"
EOF

chmod +x /usr/local/bin/wifi-audit-tool

echo "==============================="
echo "[+] Setup complete!"
echo "[+] You can now run the tool from ANYWHERE using:"
echo "    sudo wifi-audit-tool"
echo "==============================="
