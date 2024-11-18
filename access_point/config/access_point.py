import subprocess

try: 
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