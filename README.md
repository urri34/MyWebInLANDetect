# LanDeviceFinder
Contains the python scripts I use to detect my GeekMagic SmallTV-Ultra. It wakes up with DHCP and I never know where is it. It can be used to find any kind of webserver , in any kind of ip range and can detect any kind of string in the web server serving page.

## finder.py:
### Basic configuracion options:
- PORT = 80

The port where we are suposed to find teh webserver we are looking for. In the GeekMagic SmallTV-Ultra is teh tipycal 80

- StringToDetect='<meta name="author" content="GEEKMAGIC">'

String to look for in the web page we get from the thing we are looking for, you should select some line that is allways there and that should not appear in any other kind of device.

### Considerations about ip range scaned:

Depending if you hace a Win environment or a Linux environment it will work slidely different:

-  Windows

It will get the interface that is used as the default gateway (route print) and scan all that Range that is accessible with the actual IP/Mask system config (ipconfig).

```sh
Network Destination        Netmask          Gateway       Interface          Metric
          0.0.0.0          0.0.0.0      192.168.4.1    **192.168.4.234**     35
```

```sh
Wireless LAN adapter Wi-Fi:

   Connection-specific DNS Suffix  . : Home
   Link-local IPv6 Address . . . . . : cafe::cafe:cafe:cafe:cafe
   IPv4 Address. . . . . . . . . . . : 192.168.4.234
   Subnet Mask . . . . . . . . . . . : **255.255.255.0**
   Default Gateway . . . . . . . . . : 192.168.4.1
```

- Linux

It will get the interface**s** that are used as the default gateway (netstat -rn) and scan all that Range that is accessible with the actual IP/Mask system config (ip).

```sh
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
0.0.0.0         192.168.4.1     0.0.0.0         UG        0 0          0 **enp0s3**
0.0.0.0         192.168.200.1   0.0.0.0         UG        0 0          0 **wlp0s12**
```

```sh
2: enp0s3    inet **192.168.4.234/24** brd 192.168.4.255 scope global noprefixroute enp0s3\       valid_lft forever preferred_lft forever
```
