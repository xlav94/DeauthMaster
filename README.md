# DeauthMaster

## Table of Contents

1. [Description](#description)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)


## Description

**DeauthMaster** is a specialized tool for automating deauthentication attacks on WPA2 networks, particularly in environments where Wi-Fi networks are using roaming. The program automatically targets and disrupts each access point in the roaming network, effectively disconnecting devices as they transition between access points. This tool is designed to automate the process of deauthenticating devices from all access points within a roaming network, making it a powerful tool for network security assessments and understanding the vulnerabilities introduced by roaming in Wi-Fi environments.

## Prerequisites

Before installing the project, make sure you have the following installed on your system:

- Python 3
`sudo apt-get install python3.x`
- Aircrack-ng
- Wi-Fi card with monitoring mode support. Ensure that the appropriate drivers are installed for optimal functionality.

## Installation
```shell
git clone https://github.com/xlav94/DeauthMaster.git
```

## Usage

```shell
cd wifi_deauth
sudo python3 deauth_master.py
```
