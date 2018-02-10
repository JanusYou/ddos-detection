
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import ipv4
from ryu.lib.packet import arp
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
import  time
import List
from packet_in_node import Packet_In
from detect_node import DetNode
import detect_node
import detect_list
import detect
import trigger
class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    global p_number = 0

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0] #get ethernet protocol
        pkt_ipv4 = pkt.get_protocol(ipv4.ipv4) #get ipv4 protocol
        pkt_arp = pkt.get_protocol(arp.arp)
        pkt_tcp = pkt.get_protocol(tcp.tcp)
        pkt_udp = pkt.get_protocol(udp.udp)
        dst_ip = "10.10.10.10"
        src_ip = "11.11.11.11"
        dst_port = '1'
        if pkt_ipv4:      

           dst_ip = pkt_ipv4.dst
           src_ip = pkt_ipv4.src
        if pkt_arp:
           dst_ip = pkt_arp.dst_ip
           src_ip = pkt_arp.src_ip
        #else
           # return
        if not (pkt_ipv4 or pkt_arp):
           return

        if pkt_tcp:
           dst_port = pkt_tcp.dst_port

        if pkt_udp:
           dst_port = pkt_udp.dst_port

        if not(pkt_tcp or pkt_udp):
           return
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src
        #dip = ip4.dst
        #sip = ip4.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        ######create packet in node##
        newtime = time.time()
        pinode = Packey_In(newtime, dst_port, src_ip, dst_ip)
        List.pacIn_list.append(pinode)
        #####trigger###########
        global p_number
        p_number = p_number + 1
        if p_number%1000 == 0:
          dnode = DetNode(newtime, List.pacIn_list)
          flag = trigger.trigger(dnode, newtime, 120, 20)
          if flag == 0:
            alert = detect.(newnode, newtime)
            print alert
        

        self.logger.info("packet in %s %s %s %s", dpid, src_ip, dst_ip, in_port)

        # learn a ip address to avoid FLOOD next time.
        self.mac_to_port[dpid][src_ip] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst_ip]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_type=0x0800, ipv4_dst=dst_ip, ipv4_src=src_ip)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
