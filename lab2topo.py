#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink ##Think about what this does, dig around the API doc and discuss in section!
from mininet.node import RemoteController


class MyTopology(Topo):
    """
    A basic topology
    """
    def __init__(self):
        Topo.__init__(self)

        # Set Up Topology Here
        switch1 = self.addSwitch('switch1') ## Adds a Switch
        ipad = self.addHost('ipad',ip='10.1.1.1')
        self.addLink(switch1, ipad, delay='20ms')
        laptop = self.addHost('laptop',ip='10.1.1.2')
        self.addLink(switch1, laptop, delay='20ms')
        #webserver = self.addHost('webserver', ip='10.1.1.3')
        #self.addlink(switch1, webserver, delay='20ms')
        switch2 = self.addSwitch('switch2') ## Adds a Switch
        self.addLink(switch1, switch2, delay='20ms')
        lights = self.addHost('lights',ip='10.1.20.1')
        self.addLink(switch2, lights, delay='20ms')
        heater = self.addHost('heater',ip='10.1.20.2')
        self.addLink(switch2, heater, delay='20ms')
 
if __name__ == '__main__':
    """
    If this script is run as an executable (by chmod +x), this is
    what it will do
    """

    topo = MyTopology() ## Creates the topology
    c0 = RemoteController(name='c0', controller=RemoteController, ip='127.0.0.1', port=6633) #Creates a remote controller
    net = Mininet( topo=topo, controller=c0, link=TCLink ) ## Loads the topology, invokes TCLink 
    net.start() ## Starts Mininet

    # Commands here will run on the simulated topology
    CLI(net)

    net.stop() ## Stops Mininet
