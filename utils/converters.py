def cap_to_hccapx(cap_file, output_file):
    """Convert .cap file to .hccapx for hashcat"""
    import subprocess
    try:
        cmd = ["cap2hccapx", cap_file, output_file]
        subprocess.run(cmd, check=True)
        return True
    except:
        return False

def pcap_to_cap(pcap_file, output_file):
    """Convert .pcap to .cap"""
    import subprocess
    try:
        cmd = ["mergecap", "-F", "libpcap", "-w", output_file, pcap_file]
        subprocess.run(cmd, check=True)
        return True
    except:
        return False
