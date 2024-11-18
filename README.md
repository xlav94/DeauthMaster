# DeauthMaster

## Table of Contents

1. [Description](#description)
2. [Features](#features)
3. [Important](#️important-notice)  
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Usage](#usage)


## Description

**DeauthMaster** DeauthMaster is a specialized tool for automating deauthentication attacks on WPA2 networks, particularly in environments where Wi-Fi networks are using roaming. The program automatically targets and disrupts each access point in the roaming network, effectively disconnecting devices as they transition between access points. This tool is designed to automate the process of deauthenticating devices from all access points within a roaming network, making it a powerful tool for network security assessments and understanding the vulnerabilities introduced by roaming in Wi-Fi environments.

In addition to its deauthentication capabilities, DeauthMaster can also create a fake Wi-Fi access point with a captive portal. This allows for further testing and analysis by simulating a rogue network, enabling users to study potential risks such as credential harvesting and phishing attacks in controlled environments.


## Features  

**DeauthMaster** provides two powerful attack modes:  
1. **Deauthentication Attack**  
   - Disrupts connections by targeting devices on Wi-Fi networks, particularly in roaming environments.  
2. **Fake Access Point**  
   - Creates a rogue Wi-Fi network with a captive portal for security testing and analysis.  

## Important Notice  

- With a **single Wi-Fi interface**, you can perform **only one attack at a time**.  
- To execute **both attacks simultaneously**, you will need **two separate Wi-Fi interfaces**. 

## Prerequisites

Before installing the project, make sure you have the following installed on your system:

- Wi-Fi card with monitoring mode support. Ensure that the appropriate drivers are installed for optimal functionality.
- **Python 3**
`sudo apt-get install python3.x`
- **Aircrack-ng**
- **hostapd**
`sudo apt-get install hostapd`
- **iptables**
`sudo apt-get install iptables`
- **dnsmasq**
`sudo apt-get install dnsmasq`
- **flask**
`pip install flask`

## Installation
```shell
git clone https://github.com/xlav94/DeauthMaster.git
```

## Usage

### - Deauthentication attack
```shell
cd DeauthMaster
sudo python3 deauth_master.py
```
### - Fake access point
To start the wifi access point.
```shell
cd DeauthMaster/access_point/config
sudo python3 access_point.py
```
To start the web server for the captive portal. For exemple if we want to start the captive portal of 'Udem'.
```shell
cd DeauthMaster/access_point/Udem
sudo python3 main.py
```
