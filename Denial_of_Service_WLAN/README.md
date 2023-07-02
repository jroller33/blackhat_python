# Denial of Service Attack on WiFi Networks

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Disclaimer:
```diff
! Only run these scripts on networks you own or are authorized to test!
! See lines 17-21 of the LICENSE for more info.
```

## Description

These scripts are made to execute a [Denial-of-Service](https://www.cisa.gov/news-events/news/understanding-denial-service-attacks) (DoS) attack against a wireless network (i.e. they'll crash a wifi network). 

They will only run on [Kali Linux](https://www.kali.org/). I recommend creating a virtual machine and installing kali on the vm.




## Usage

**Please note: these scripts require a wireless adapter that supports both monitor mode and injection mode.**
(The wireless adapters in most laptops don't support monitor and injection modes.)

If you have a windows machine, you can test your wireless adapter's capabilities like this:

1. Open powershell or command prompt in administrator mode
2. run `netsh`
3. run `wlan show wirelesscapabilities`
4. In the list that's shown, Network monitor mode will show "Supported" or "Not Supported"

If your wireless adapter doesn't support these modes, you can buy one. [Click here for more info](https://null-byte.wonderhowto.com/how-to/select-field-tested-kali-linux-compatible-wireless-adapter-0180076/).



## Contribution
You can contribute by forking this [repo](https://github.com/jroller33/WiFi_DoS_Attack) and submitting a pull request.

## License
This project is licensed under the [MIT License](./LICENSE).

## Contact
[GitHub](https://github.com/jroller33)

