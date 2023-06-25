# Black Hat Hacking with Python

## Setup

This requires Kali Linux running inside a virtual machine. You'll need a hypervisor virtualization client also (like VMware, VirtualBox or Hyper-V).
<br />
On my computer (Windows 11 x64, v10.0.22621) I followed these steps to setup the VM and Kali Linux:


- Make sure Virtualization is ENABLED in your system BIOS/UEFI.

- Turn on "Windows Hypervisor Platform" in "Turn Windows Features on or off"

- Download "VMware Workstation 17.0.2 Player" [(this version is FREE)](https://customerconnect.vmware.com/en/downloads/details?downloadGroup=WKST-PLAYER-1702&productId=1377&rPId=104734)

- Download [Kali Linux ISO](https://www.kali.org/get-kali/#kali-installer-images)

- Follow these steps to create the VM: [Kali VMware Docs](https://www.kali.org/docs/virtualization/install-vmware-guest-vm/)

- Follow these steps (inside the VM) to complete installation: [Kali Installation](https://www.kali.org/docs/installation/hard-disk-install/)

- Now you should have a virtual machine with Kali Linux installed!

- Next open a terminal in your Kali VM and run these commands to install and update the packages:

```
sudo apt update
apt list --upgradable
sudo apt upgrade
sudo apt dist-upgrade
sudo apt autoremove
```

- Check which Python version is installed:
```
python3
```

- You need Python version 3.7 or higher. If you need to upgrade your version, run this command:

```
sudo apt-get upgrade python3
```
- Then install the Python package for virtual environments:
```
sudo apt-get install python3-venv
```

- Make a new directory to work in and create a virtual environment:
```
mkdir mynewfolder
cd mynewfolder
python3 -m venv venv3
source venv3/bin/activate
python
```