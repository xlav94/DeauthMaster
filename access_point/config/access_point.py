import subprocess
import re

def check_ip(interface):
    try:
        # Execute the `ip addr show` command for the specified interface
        result = subprocess.run(['ip', 'addr', 'show', interface], capture_output=True, text=True)
        
        # If the command succeeds, it contains information about the interface
        if result.returncode == 0:
            # Search for the line containing 'inet' (IPv4 address)
            match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', result.stdout)
            if match:
                # Return the IP address found
                return True
            else:
                # No IPv4 address found
                return False
        else:
            # In case of an error (e.g., interface doesn't exist)
            print(f"Error: Could not retrieve address for interface {interface}")
            return False
    except Exception as e:
        print(f"Error executing the command: {e}")
        return False
    
try:
    if check_ip("wlan0"):
        set_ip_interface = subprocess.run(["ip", "addr", "flush", "dev", "wlan0"], check=True)
    set_ip_interface = subprocess.run(["ip", "addr", "add", "192.168.1.1/24", "dev", "wlan0"], check=True)
    stop_dnsmasq = subprocess.run(["systemctl", "stop", "dnsmasq"], check=True) 
    stop_hostapd = subprocess.run(["systemctl", "stop", "hostapd"], check=True)

    subprocess.run(["iptables", "-F"], check=True)
    subprocess.run(["iptables", "-t", "nat", "-F"], check=True)
    subprocess.run(["iptables", "-X"], check=True)
    subprocess.run(["iptables", "-t", "nat", "-X"], check=True)
    subprocess.run(
                ["iptables", "-t", "nat", "-A", "PREROUTING", "-i", "wlan0", "-p", "tcp", "--dport", "80", "-j", "DNAT", "--to-destination", "192.168.56.128:80"],
                check=True
            )
    subprocess.run(["iptables", "-t", "nat", "-A", "POSTROUTING", "-j", "MASQUERADE"], check=True)

    subprocess.run(["dnsmasq", "-C", "dnsmasq.conf"], check=True)
    subprocess.run(["hostapd", "hostapd.conf"], check=True)
    
    print("All commands were executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error while executing the command: {e.cmd}")
    print(f"Return code: {e.returncode}")
except FileNotFoundError as e:
    print(f"File not found: {e.filename}")
    
except KeyboardInterrupt:
    print("Stopping the access point...")