import subprocess


ip addr add 192.168.1.1/24 dev wlan0
systemctl stop dnsmasq  
systemctl stop hostapd

iptables -F 
iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 80 -j DNAT --to-destination 192.168.56.128:80
iptables -t nat -A POSTROUTING -j MASQUERADE   

dnsmasq -C dnsmasq.conf
hostapd hostapd.conf