ip_header = packet.find('ipv4')

iPadAddr =   "10.1.1.1"
laptopAddr = "10.1.1.2"
lightsAddr = "10.1.20.1"
heaterAddr = "10.1.20.2"

# allow ARP any/any
if packet.find('arp') is not None:
    accept()

# allow ICMP any/any
elif packet.find('icmp') is not None:
    accept()

# allow TCP laptop/iPad
elif ip_header.srcip == laptopAddr and ip_header.dstip == iPadAddr and packet.find('tcp') is not None:
    accept()

# allow TCP iPad/laptop
elif ip_header.srcip == iPadAddr and ip_header.dstip == laptopAddr and packet.find('tcp') is not None:
    accept()

# allow TCP iPad/lights
elif ip_header.srcip == iPadAddr and ip_header.dstip == lightsAddr and packet.find('tcp') is not None:
    accept()

# allow TCP iPad/heater
elif ip_header.srcip == iPadAddr and ip_header.dstip == heaterAddr and packet.find('tcp') is not None:
    accept()

# allow UDP heater/lights
elif ip_header.srcip == heaterAddr and ip_header.dstip == lightsAddr and packet.find('udp') is not None:
    accept()

# allow UDP laptop/ipad
elif ip_header.srcip == laptopAddr and ip_header.dstip == iPadAddr and packet.find('udp') is not None:
    accept()

# drop all others
else:
    drop()
