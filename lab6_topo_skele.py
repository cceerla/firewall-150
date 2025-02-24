#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController

class MyTopology(Topo):
  def __init__(self):
    Topo.__init__(self)
   
    # laptop1 = self.addHost('Laptop1', ip='200.20.2.8/24',defaultRoute="Laptop1-eth1")
    # switch1 = self.addSwitch('s1')
    # self.addLink(laptop1, switch1, port1=1, port2=2)
    
    # blue
    s1 = self.addSwitch('s1')
    trustedPC1 = self.addHost('trustedPC1', ip='212.26.59.102/32', defaultRoute="trustedPC1-eth6")
    self.addLink(trustedPC1, s1, port1=6, port2=9)
    trustedPC2 = self.addHost('trustedPC2', ip='10.100.198.6/32', defaultRoute="trustedPC2-eth6")
    self.addLink(trustedPC2, s1, port1=6, port2=8)
    guest = self.addHost('guest', ip='10.100.198.10/32', defaultRoute="guest-eth6")
    self.addLink(guest, s1, port1=6, port2=7)

    # red
    s2 = self.addSwitch('s2')
    self.addLink(s2, s1, port1=6, port2=2)
    facultyWS = self.addHost('facultyWS', ip='169.233.3.10/24', defaultRoute="facultyWS-eth2")
    self.addLink(facultyWS, s2, port1=2, port2=9)
    printer = self.addHost('printer', ip='169.233.3.20/24', defaultRoute="printer-eth2")
    self.addLink(printer, s2, port1=2, port2=8)
    facultyPC = self.addHost('facultyPC', ip='169.233.3.30/24', defaultRoute="facultyPC-eth2")
    self.addLink(facultyPC, s2, port1=2, port2=7)

    # yellow
    s5 = self.addSwitch('s5')
    self.addLink(s1, s5, port1=3, port2=6)
    examServer = self.addHost('examServer', ip='169.233.2.1/24', defaultRoute="examServer-eth3")
    self.addLink(examServer, s5, port1=3, port2=9)
    webServer = self.addHost('webServer', ip='169.233.2.2/24', defaultRoute="webServer-eth3")
    self.addLink(webServer, s5, port1=3, port2=8)
    dnsServer = self.addHost('dnsServer', ip='169.233.2.3/24', defaultRoute="dnsServer-eth3")
    self.addLink(dnsServer, s5, port1=3, port2=7)

    # purple
    s4 = self.addSwitch('s4')
    self.addLink(s1, s4, port1=4, port2=6)
    itBackup = self.addHost('itBackup', ip='169.233.1.30/24', defaultRoute="itBackup-eth4")
    self.addLink(itBackup, s4, port1=4, port2=7)
    itWS = self.addHost('itWS', ip='169.233.1.10/24', defaultRoute="itWS-eth4")
    self.addLink(itWS, s4, port1=4, port2=9)
    itPC = self.addHost('itPC', ip='169.233.1.20/24', defaultRoute="itPC-eth4")
    self.addLink(itPC, s4, port1=4, port2=8)

    # green
    s3 = self.addSwitch('s3')
    self.addLink(s1, s3, port1=5, port2=6)
    studentPC1 = self.addHost('studentPC1', ip='169.233.4.1/24', defaultRoute="studentPC1-eth5")
    self.addLink(studentPC1, s3, port1=5, port2=9)
    studentPC2 = self.addHost('studentPC2', ip='169.233.4.2/24', defaultRoute="studentPC2-eth5")
    self.addLink(studentPC2, s3, port1=5, port2=8)
    labWS = self.addHost('labWS', ip='169.233.4.100/24', defaultRoute="labWS-eth5")
    self.addLink(labWS, s3, port1=5, port2=7)

    # discord server
    s6 = self.addSwitch('s6')
    self.addLink(s1, s6, port1=100, port2=6)
    dServer = self.addHost('dServer', ip='13.61.7.1/24', defaultRoute="dServer-eth9")
    self.addLink(dServer, s6, port1=100, port2=9)
    
if __name__ == '__main__':
  #This part of the script is run when the script is executed
  topo = MyTopology() #Creates a topology
  #c0 = RemoteController(name='c0', controller=RemoteController, ip='127.0.0.1', port=6633) #Creates a remote controller
  #net = Mininet(topo=topo, controller=c0) #Loads the topology
  net = Mininet(topo=topo) #Loads the topology
  net.start() #Starts mininet
  CLI(net) #Opens a command line to run commands on the simulated topology
  net.stop() #Stops mininet
