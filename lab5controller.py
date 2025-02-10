# Lab 5 controller skeleton 
#
# Based on of_tutorial by James McCauley



from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt

log = core.getLogger()

class Firewall (object):
    """
    A Firewall object is created for each switch that connects.
    A Connection object for that switch is passed to the __init__ function.
    """
    def __init__ (self, connection):
        # Keep track of the connection to the switch so that we can
        # send it messages!
        self.connection = connection
        self.transparent = transparent
        
        # Our table
        self.macToPort = {}
        
        # This binds our PacketIn event listener
        connection.addListeners(self)
        
    def do_firewall (self, packet, packet_in):
        # The code in here will be executed for every packet
       
        # pkt is like event in l2_learning
        # pkt_in is the output (?)

        timeout_idle = 60
        timeout_hard = 60 * 5
        
        def accept(packet, packet_in):
            # Write code for an accept function
            msg = of.ofp_flow_mod()
            msg.data = packet_in
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = timeout_idle
            msg.hard_timeout = timeout_hard
            # this makes it put the packet into a port
            msg.actions.append(of.ofp_action_output(port=of.OFPP_NORMAL))
            msg.buffer_id = packet_in.buffer_id
            self.connection.send(msg)
            
            print("Packet Accepted - Flow Table Installed on Switches")
            
        def drop(packet):
            # we do not have a duration because the
            #   idle/hard timeout is hardcoded
            # this is stolen wholesale from l2_learning.py 
            if event.ofp.buffer_id is not None:
                msg = of.ofp_packet_out()
                msg.match = of.ofp_match.from_packet(packet.parsed)
                msg.idle_timeout = timeout_idle
                msg.hard_timeout = timeout_hard
                msg.buffer_id = packet.ofp.buffer_id
                msg.in_port = packet.port
                self.connection.send(msg)
            print("Packet Dropped - Flow Table Installed on Switches")
            
            # Write firewall code 
            print("Example Code")
            
        # Hints:
        #
        # To check the source and destination of an IP packet, you can use
        # the header information... For example:
        #
        # ip_header = packet.find('ipv4')
        #
        # if ip_header.srcip == "1.1.1.1":
        #   print "Packet is from 1.1.1.1"
        #
        # Important Note: the "is" comparison DOES NOT work for IP address
        # comparisons in this way. You must use ==.
        #
        # To drop packets, simply omit the action .
        
        # firewall rules ----------------------------------
        
        accept()
        
    def _handle_PacketIn (self, event):
        """
        Handles packet in messages from the switch.
        """

        packet = event.parsed # This is the parsed packet data.
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return
        
        packet_in = event.ofp # The actual ofp_packet_in message.
        self.do_firewall(packet, packet_in)
        
    def launch ():
        """
        Starts the components
        """
    def start_switch (event):
        log.debug("Controlling %s" % (event.connection,))
        Firewall(event.connection)
        core.openflow.addListenerByName("ConnectionUp", start_switch)
