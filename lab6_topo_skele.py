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
    
    # red
    s2 = self.addSwitch('s2')
    facultyWS = self.addHost('facultyWS', ip='169.233.3.10/24', defaultRoute="facultyWS-eth15")
    self.addLink(facultyWS, s2, port1=15, port2=2)
    printer = self.addHost('printer', ip='169.233.3.20/24', defaultRoute="printer-eth14")
    self.addLink(printer, s2, port1=14, port2=2)
    facultyPC = self.addHost('facultyPC', ip='169.233.3.30/24', defaultRoute="facultyPC-eth13")
    self.addLink(facultyPC, s2, port1=13, port2=2)
    
    # yellow
    s5 = self.addSwitch('s5')
    examServer = self.addHost('examServer', ip='169.233.2.1/24', defaultRoute="examServer-eth15")
    self.addLink(examServer, s2, port1=15, port2=3)
    webServer = self.addHost('webServer', ip='169.233.2.2/24', defaultRoute="webServer-eth14")
    self.addLink(webServer, s2, port1=14, port2=3)
    dnsServer = self.addHost('dnsServer', ip='169.233.2.3/24', defaultRoute="dnsServer-eth13")
    self.addLink(dnsServer, s2, port1=13, port2=3)
    
    # purple
    s4 = self.addSwitch('s4')
    itBackup = self.addHost('itBackup', ip='169.233.1.30/24', defaultRoute="itBackup-eth13")
    self.addLink(itBackup, s2, port1=13, port2=4)
    itWS = self.addHost('itWS', ip='169.233.1.10/24', defaultRoute="itWS-eth15")
    self.addLink(itWS, s2, port1=15, port2=4)
    itPC = self.addHost('itPC', ip='169.233.1.20/24', defaultRoute="itPC-eth14")
    self.addLink(itPC, s2, port1=14, port2=4)
    
    # green
    s3 = self.addSwitch('s3')
    studentPC1 = self.addHost('studentPC1', ip='169.233.4.1/24', defaultRoute="studentPC1-eth15")
    self.addLink(studentPC1, s2, port1=15, port2=5)
    studentPC2 = self.addHost('studentPC2', ip='169.233.4.2/24', defaultRoute="studentPC2-eth14")
    self.addLink(studentPC2, s2, port1=14, port2=5)
    labWS = self.addHost('labWS', ip='169.233.4.100/24', defaultRoute="labWS-eth13")
    self.addLink(labWS, s2, port1=13, port2=5)
    
    # blue
    s1 = self.addSwitch('s1')
    trustedPC1 = self.addHost('trustedPC1', ip='212.26.50.??/32', defaultRoute="trustedPC1-eth15")
    self.addLink(trustedPC1, s2, port1=15, port2=6)
    trustedPC2 = self.addHost('trustedPC2', ip='10.100.136.632/32', defaultRoute="trustedPC2-eth13")
    self.addLink(trustedPC2, s2, port1=13, port2=6)
    guest = self.addHost('guest', ip='10.100.136.1032/32', defaultRoute="guest-eth14")
    self.addLink(guest, s2, port1=14, port2=6)
    
if __name__ == '__main__':
  #This part of the script is run when the script is executed
  topo = MyTopology() #Creates a topology
  c0 = RemoteController(name='c0', controller=RemoteController, ip='127.0.0.1', port=6633) #Creates a remote controller
  net = Mininet(topo=topo, controller=c0) #Loads the topology
  net.start() #Starts mininet
  CLI(net) #Opens a command line to run commands on the simulated topology
  net.stop() #Stops mininet
