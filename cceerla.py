# Copyright 2011 James McCauley
#
# This file is part of POX.
#
# POX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# POX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with POX.  If not, see <http://www.gnu.org/licenses/>.

"""
An L2 learning switch.

It is derived from one written live for an SDN crash course.
It is somwhat similar to NOX's pyswitch in that it installs
exact-match rules for each flow.
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
import time

log = core.getLogger()

_timeout_idle = 60
_timeout_hard = 60 * 5

# We don't want to flood immediately when a switch connects.
# Can be overriden on commandline.
_flood_delay = 0

class Firewall (object):
    def __init__ (self, connection, transparent):
        # Switch we'll be adding L2 learning switch capabilities to
        self.connection = connection
        self.transparent = transparent

        # Our table
        self.macToPort = {}

        # We want to hear PacketIn messages, so we listen
        # to the connection
        connection.addListeners(self)

        # We just use this to know when to log a helpful message
        self.hold_down_expired = _flood_delay == 0

        #log.debug("Initializing Firewall, transparent=%s",
        #          str(self.transparent))
    
    def do_firewall(self, packet, packet_in):
        # execute this in handle_pktIn
        # pkt is like event in l2_learning
        # pkt_in is the output (?)


        def accept(packet, packet_in):
            # Write code for an accept function
            msg = of.ofp_flow_mod()
            msg.data = packet_in
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = _timeout_idle
            msg.hard_timeout = _timeout_hard
            # this makes it put the packet into a port
            msg.actions.append(of.ofp_action_output(port=of.OFPP_NORMAL))
            msg.buffer_id = packet_in.buffer_id
            self.connection.send(msg)
            
            print("Packet Accepted - Flow Table Installed on Switches")
         
        def drop(packet, packet_in):
            # we do not have a duration because the
            #   idle/hard timeout is hardcoded
            # this is stolen wholesale from l2_learning.py 
            if packet_in.buffer_id is not None:
                msg = of.ofp_packet_out()
                msg.match = of.ofp_match.from_packet(packet.parsed)
                msg.idle_timeout = _timeout_idle
                msg.hard_timeout = _timeout_hard
                msg.buffer_id = packet.ofp.buffer_id
                msg.in_port = packet.port
                self.connection.send(msg)
            print("Packet Dropped - Flow Table Installed on Switches")
        log.warning("Beginning firewall rules...")
        
        drop(packet, packet_in)
        
        return

    def _handle_PacketIn (self, event):
        """
        Handle packet in messages from the switch to implement above algorithm.
        """

        packet = event.parsed
        if not packet.parsed:
            log.warning("Incomplete Packet: Skipping this")
            return
        packet_in = event.ofp
        
        self.do_firewall(packet, packet_in)
        """
        self.macToPort[packet.src] = event.port # 1

        if not self.transparent: # 2
            if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered():
                drop() # 2a
                return

        if packet.dst.is_multicast:
            flood() # 3a
        else:
            if packet.dst not in self.macToPort: # 4
                flood("Port for %s unknown -- flooding" % (packet.dst,)) # 4a
            else:
                port = self.macToPort[packet.dst]
                if port == event.port: # 5
                    # 5a
                    log.warning("Same port for packet from %s -> %s on %s.%s.  Drop."
                        % (packet.src, packet.dst, dpid_to_str(event.dpid), port))
                    drop(10)
                    return
                # 6
                log.debug("installing flow for %s.%i -> %s.%i" %
                          (packet.src, event.port, packet.dst, port))
                msg = of.ofp_flow_mod()
                msg.match = of.ofp_match.from_packet(packet, event.port)
                msg.idle_timeout = 10
                msg.hard_timeout = 30
                msg.actions.append(of.ofp_action_output(port = port))
                msg.data = event.ofp # 6a
                self.connection.send(msg)
        """

class l2_learning (object):
    """
    Waits for OpenFlow switches to connect and makes them learning switches.
    """
    def __init__ (self, transparent):
        core.openflow.addListeners(self)
        self.transparent = transparent

    def _handle_ConnectionUp (self, event):
        log.debug("Connection %s" % (event.connection,))
        Firewall(event.connection, self.transparent)


def launch (transparent=False, hold_down=_flood_delay):
    """
    Starts an L2 learning switch.
    """
    try:
        global _flood_delay
        _flood_delay = int(str(hold_down), 10)
        assert _flood_delay >= 0
    except:
        raise RuntimeError("Expected hold-down to be a number")

    core.registerNew(l2_learning, str_to_bool(transparent))
    """
        def flood (message = None):
            msg = of.ofp_packet_out()
            if time.time() - self.connection.connect_time >= _flood_delay:
                # Only flood if we've been connected for a little while...

                if self.hold_down_expired is False:
                    # Oh yes it is!
                    self.hold_down_expired = True
                    log.info("%s: Flood hold-down expired -- flooding",
                        dpid_to_str(event.dpid))

                if message is not None: log.debug(message)
                #log.debug("%i: flood %s -> %s", event.dpid,packet.src,packet.dst)
                # OFPP_FLOOD is optional; on some switches you may need to change
                # this to OFPP_ALL.
                msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
            else:
                pass
                #log.info("Holding down flood for %s", dpid_to_str(event.dpid))
            msg.data = event.ofp
            msg.in_port = event.port
            self.connection.send(msg)
        """

