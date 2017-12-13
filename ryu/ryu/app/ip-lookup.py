# IMPORT LIBRARIES
import json
from webob import Response
from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet.packet import Packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import arp
from ryu.lib.packet import ipv4
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
from ryu.lib.packet import ether_types
from ryu.ofproto import ether
from ryu.app.ofctl.api import get_datapath
from binary_tree import BinaryTree,DisjointBT,CompleteBT,Node
from binary_search import prefixLengthBS, prefixLengthExpandBS, prefixRangeBS
import os
import time,datetime
# REST API for switch configuration
#
# get switches
# GET /v1.0/lookup/switches
#
# get bridge-table
# GET /v1.0/lookup/bridge-table
#
# get lookup
# GET /v1.0/lookup/lookup
#
# get ip-to-mac
# GET /v1.0/lookup/ip-to-mac

IP     = 0
SUBNET = 1
MAC    = 2
NAME   = 3
DPID   = 4
ALGORITHM = 1 # 1: BINARY TREE |2: COMPLETE BT |3: DISJOINT BT |4: PREFIX LENGTH BINARY SEARCH WITH MARKERS|
              # 5: PREFIX LENGTH BINARY SEARCH WITH EXPANSION |6: PREFIX RANGE BS
# Main class for switch
def get_alg_name(argument):
    switcher = {
        1: "BINARY-TREE",
        2: "COMPLETE-BINARY-TREE",
        3: "DISJOINT-BINARY-TREE",
        4: "PREFIX-LENGTH-MARKER",
        5: "PREFIX-LENGTH-EXPAND",
        6: "PREFIX-RANGE"
    }
    return switcher.get(argument, "nothing")
class SimpleSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]
    _CONTEXTS = {
        'wsgi': WSGIApplication
    }

    # Initialize the application 
    def __init__(self, *args, **kwargs):
        super(SimpleSwitch, self).__init__(*args, **kwargs)
        wsgi = kwargs['wsgi']
        wsgi.register(LookupController, {'lookup_api_app': self})

        # Add all initialization code here
        self.searches = 0 
        self.alltime = 0
        self.avgtime = 0
        self.logfile = open(get_alg_name(ALGORITHM)+".txt","w")

        self.mac_to_port = {} 
        self.mac_to_port["1"] = {}
        self.mac_to_port["2"] = {}
        self.mac_to_port["3"] = {}
        self.mac_to_port["4"] = {}
        self.mac_to_port["5"] = {}
        self.mac_to_port["6"] = {}
        self.mac_to_port["7"] = {}
        self.mac_to_port["8"] = {}
        self.mac_to_port["9"] = {}
        self.mac_to_port["10"] = {}
        self.mac_to_port["11"] = {}
        self.mac_to_port["12"] = {}
        self.mac_to_port["13"] = {}
        self.mac_to_port["14"] = {}
        self.mac_to_port["15"] = {}
        self.mac_to_port["16"] = {}

        self.mac_to_port["1"]["00:00:00:00:00:01"] = 1
        self.mac_to_port["1"]["00:00:00:00:00:02"] = 2
        self.mac_to_port["1"]["00:00:00:00:00:03"] = 3
        self.mac_to_port["1"]["00:00:00:00:00:04"] = 4
        
        self.mac_to_port["2"]["00:00:00:00:00:05"] = 1
        self.mac_to_port["2"]["00:00:00:00:00:06"] = 2
        self.mac_to_port["2"]["00:00:00:00:00:07"] = 3
        self.mac_to_port["2"]["00:00:00:00:00:08"] = 4
        
        self.mac_to_port["3"]["00:00:00:00:00:09"] = 1
        self.mac_to_port["3"]["00:00:00:00:00:0A"] = 2
        
        self.mac_to_port["4"]["00:00:00:00:00:0B"] = 1
        self.mac_to_port["4"]["00:00:00:00:00:0C"] = 2
        self.mac_to_port["4"]["00:00:00:00:00:0D"] = 3
        
        self.mac_to_port["5"]["00:00:00:00:00:0E"] = 1
        self.mac_to_port["5"]["00:00:00:00:00:0F"] = 2
        self.mac_to_port["5"]["00:00:00:00:00:10"] = 3
        
        
        self.mac_to_port["6"]["00:00:00:00:00:11"] = 1
        self.mac_to_port["6"]["00:00:00:00:00:12"] = 2

        self.mac_to_port["7"]["00:00:00:00:00:13"] = 1
        self.mac_to_port["7"]["00:00:00:00:00:14"] = 2

        self.mac_to_port["8"]["00:00:00:00:00:15"] = 1
        self.mac_to_port["8"]["00:00:00:00:00:16"] = 2


        self.switch = {}
        self.switch["10.0.0.254"] = ["10.0.0.254","","33:33:00:00:00:01","s1","1"]
        self.switch["172.16.0.254"] = ["172.16.0.254","16","33:33:00:00:00:02","s2","2"]
        self.switch["195.169.1.254"] = ["195.169.1.254","24","33:33:00:00:00:03","s3","3"]
        self.switch["156.16.16.254"] = ["156.16.16.254","12","33:33:00:00:00:04","s4","4"]
        self.switch["192.168.2.254"] = ["192.168.2.254","24","33:33:00:00:00:05","s5","5"]
        self.switch["128.128.0.254"] = ["128.128.0.254","16","33:33:00:00:00:06","s6","6"]
        self.switch["137.168.1.254"] = ["137.168.1.254","8","33:33:00:00:00:07","s7","7"]
        self.switch["10.12.12.254"] = ["10.12.12.254","16","33:33:00:00:00:08","s8","8"]

        self.lookup = {}
        self.lookup["10.0.0.1"] = "10.0.0.254"
        self.lookup["10.0.0.2"] = "10.0.0.254"
        self.lookup["10.0.0.3"] = "10.0.0.254"
        self.lookup["10.0.0.4"] = "10.0.0.254"
        self.lookup["172.16.0.1"] = "172.16.0.254"
        self.lookup["172.16.0.2"] = "172.16.0.254"
        self.lookup["172.16.0.3"] = "172.16.0.254"
        self.lookup["172.16.0.4"] = "172.16.0.254"
        self.lookup["195.169.1.1"] = "195.169.1.254"
        self.lookup["195.169.1.2"] = "195.169.1.254"
        self.lookup["156.16.16.1"] = "156.16.16.254"
        self.lookup["156.16.16.2"] = "156.16.16.254"
        self.lookup["156.16.16.3"] = "156.16.16.254"
        self.lookup["192.168.2.1"] = "192.168.2.254"
        self.lookup["192.168.2.2"] = "192.168.2.254"
        self.lookup["192.168.2.3"] = "192.168.2.254"
        self.lookup["128.128.0.1"] = "128.128.0.254"
        self.lookup["128.128.0.2"] = "128.128.0.254"
        self.lookup["137.168.1.1"] = "137.168.1.254"
        self.lookup["137.168.1.2"] = "137.168.1.254"
        self.lookup["10.12.12.1"] = "10.12.12.254" 
        self.lookup["10.12.12.2"] = "10.12.12.254"

        self.ip_to_mac = {}
        self.ip_to_mac["10.0.0.1"] = "00:00:00:00:00:01"
        self.ip_to_mac["10.0.0.2"] = "00:00:00:00:00:02"
        self.ip_to_mac["10.0.0.3"] = "00:00:00:00:00:03"
        self.ip_to_mac["10.0.0.4"] = "00:00:00:00:00:04"

        self.ip_to_mac["172.16.0.1"] = "00:00:00:00:00:05"
        self.ip_to_mac["172.16.0.2"] = "00:00:00:00:00:06"
        self.ip_to_mac["172.16.0.3"] = "00:00:00:00:00:07"
        self.ip_to_mac["172.16.0.4"] = "00:00:00:00:00:08"

        self.ip_to_mac["195.169.1.1"] ="00:00:00:00:00:09"
        self.ip_to_mac["195.169.1.2"] ="00:00:00:00:00:0A"

        self.ip_to_mac["156.16.16.1"] ="00:00:00:00:00:0B"
        self.ip_to_mac["156.16.16.2"] ="00:00:00:00:00:0C"
        self.ip_to_mac["156.16.16.3"] ="00:00:00:00:00:0D"
        
        self.ip_to_mac["192.168.2.1"] ="00:00:00:00:00:0E"
        self.ip_to_mac["192.168.2.2"] ="00:00:00:00:00:0F"
        self.ip_to_mac["192.168.2.3"] ="00:00:00:00:00:10"

        self.ip_to_mac["128.128.0.1"] ="00:00:00:00:00:11"
        self.ip_to_mac["128.128.0.2"] ="00:00:00:00:00:12"

        self.ip_to_mac["137.168.1.1"] ="00:00:00:00:00:13"
        self.ip_to_mac["137.168.1.2"] ="00:00:00:00:00:14"

        self.ip_to_mac["10.12.12.1"] = "00:00:00:00:00:15"
        self.ip_to_mac["10.12.12.2"] = "00:00:00:00:00:16"

        self.generate_tree()


        ''' v3
        self.mac_to_port = {}
        '''

        ''' v4
        self.filter      = {"00:00:00:00:00:03"} 
        '''


    ''' v5''' 
    def add_flow(self, datapath, in_port, dst, actions):
        ofproto = datapath.ofproto

        match = datapath.ofproto_parser.OFPMatch(
            in_port=in_port, dl_dst=haddr_to_bin(dst))

        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=ofproto.OFP_DEFAULT_PRIORITY,
            flags=ofproto.OFPFF_SEND_FLOW_REM, actions=actions)
        self.logger.info("  --> Installing flow: Switch[%s], IN port[%s], Dst MAC[%s]",\
            datapath.id,in_port,dst)
        datapath.send_msg(mod)

    def generate_tree(self):
        self.table = {}
        filepath = os.path.dirname(__file__)+"/routingtable.txt"
        f = open(filepath,'r')
        max_prefix_length = 0
        for line in f:
            line = line.rstrip("\n\r")
            [srcIP_net, nextHop] = line.split(' ')
            [srcIP,subnet] = srcIP_net.split("/")
            prefix = ''.join(format(int(x),'08b') for x in srcIP.split('.'))
            subnet = int(subnet)
            prefix = prefix[0:subnet]
            self.table[prefix] = nextHop
            if len(prefix) > max_prefix_length:
                max_prefix_length = len(prefix)
        f.close()
        if ALGORITHM == 1:
            self.tree = BinaryTree(self.table)
        if ALGORITHM == 2:
            self.tree = CompleteBT(max_prefix_length,self.table)
        if ALGORITHM == 3:
            self.tree = DisjointBT(self.table)
        if ALGORITHM == 4:
            self.tree = prefixLengthBS(max_prefix_length,self.table)
        if ALGORITHM == 5:
            self.tree = prefixLengthExpandBS(max_prefix_length,self.table)
        if ALGORITHM == 6:
            self.tree = prefixRangeBS(max_prefix_length,self.table)

    def to_binary(self,srcIP):
        return ''.join(format(int(x),'08b') for x in srcIP.split('.'))
        
    def send_arp_reply(self, datapath, srcMac, srcIp, dstMac, dstIp, outPort):
        e = ethernet.ethernet(dstMac, srcMac, ether.ETH_TYPE_ARP)
        a = arp.arp(1, 0x0800, 6, 4, 2, srcMac, srcIp, dstMac, dstIp)
        p = Packet()
        p.add_protocol(e)
        p.add_protocol(a)
        p.serialize()

        actions = [datapath.ofproto_parser.OFPActionOutput(outPort, 0)]
        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=0xffffffff,
            in_port=datapath.ofproto.OFPP_CONTROLLER,
            actions=actions,
            data=p.data)
        datapath.send_msg(out)

    def send_port_stats_request(self, datapath):
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        req = ofp_parser.OFPPortStatsRequest(datapath, 0, ofp.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def port_stats_reply_handler(self, ev):
        self.logger.info("***********port stat reply ")
        msg = ev.msg
        ofp = msg.datapath.ofproto
        body = ev.msg.body

        ports = []
        for stat in body:
            ports.append('port_no=%d '
                         'rx_packets=%d tx_packets=%d '
                         'rx_bytes=%d tx_bytes=%d '
                         'rx_dropped=%d tx_dropped=%d '
                         'rx_errors=%d tx_errors=%d '
                         'rx_frame_err=%d rx_over_err=%d rx_crc_err=%d '
                         'collisions=%d' %
                         (stat.port_no,
                          stat.rx_packets, stat.tx_packets,
                          stat.rx_bytes, stat.tx_bytes,
                          stat.rx_dropped, stat.tx_dropped,
                          stat.rx_errors, stat.tx_errors,
                          stat.rx_frame_err, stat.rx_over_err,
                          stat.rx_crc_err, stat.collisions))
        self.logger.debug('PortStats: %s', ports)

    # Register PACKET HANDLER
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg                          # OpenFlow event message
        datapath = msg.datapath               # Switch class that received the packet   
        ofproto = datapath.ofproto            # OpenFlow protocol class  

        # Parse packet
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        # Ignore lldp packet
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return

        dst = eth.dst
        src = eth.src
        dpid = datapath.id
        self.logger.info("--Packet IN: Switch id[%s], Src MAC[%s], Dst MAC[%s], Port[%s]", dpid, src, dst, msg.in_port)
        action = "allow"

        if dst == 'ff:ff:ff:ff:ff:ff': 
            self.logger.info("  Broadcast packet")
            if eth.ethertype == ether_types.ETH_TYPE_ARP:
                self.logger.info("  eth.ethertype: %s ",eth.ethertype)
                arp_packet = pkt.get_protocol(arp.arp)
                if arp_packet.opcode == 1: #request
                    arp_dst_ip = arp_packet.dst_ip
                    arp_src_ip = arp_packet.src_ip
                    self.logger.info("  Received ARP request for dst IP %s" % arp_dst_ip)
                    if arp_dst_ip in self.switch:
                        switch_mac = self.switch[arp_dst_ip][MAC]

                        self.send_arp_reply(datapath,switch_mac,arp_dst_ip,src,arp_src_ip,msg.in_port) 
                        self.logger.info("  Sent gratious ARP reply [%s]-[%s] to %s " % 
                                         (arp_packet.dst_ip,switch_mac,arp_packet.src_ip))  

                        return 0


            actions = [datapath.ofproto_parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
            data = None
            if msg.buffer_id == ofproto.OFP_NO_BUFFER:   #packet is not buffered on switch
                data = msg.data

            out = datapath.ofproto_parser.OFPPacketOut(
                datapath=datapath, buffer_id=msg.buffer_id, in_port=msg.in_port,
                actions=actions, data=data)
            self.logger.info("  Flooding packet to all other ports")
            #self.send_port_stats_request(datapath)
            datapath.send_msg(out)
            return


        ip4_pkt = pkt.get_protocol(ipv4.ipv4)
        if ip4_pkt:
            self.logger.info("  --- IP LOOKUP")
            src_ip = ip4_pkt.src
            dst_ip = ip4_pkt.dst
            self.logger.info("  --- src_ip[%s], dst_ip[%s]" % (src_ip,dst_ip))

            beginning = datetime.datetime.now()
            sw = self.tree.search(self.to_binary(dst_ip))
            end = datetime.datetime.now()
            timeNeeded = (end-beginning).total_seconds()*1000
            
            self.searches  = self.searches +1
            self.alltime  = self.alltime + timeNeeded
            self.avgtime = self.alltime/self.searches 

            self.logfile.write("on search " + str(self.searches) + " --> " + str(timeNeeded)+"s\n")
            self.logfile.write("AVG " + str(self.searches) + " --> " + str(self.avgtime)+"s\n")

            self.logger.info("Search Time =  %s" % self.avgtime)
            #if dst_ip in self.lookup:
            if sw != None:
                sw = self.lookup[dst_ip]
                self.logger.info("  --- Destination present on switch %s" % (self.switch[sw]))
                dp = get_datapath(self,int(self.switch[sw][DPID]))
                self.logger.info("self.switch[sw][DPID] %s self.ip_to_mac[dst_ip %s" % (self.switch[sw][DPID],self.ip_to_mac[dst_ip]))
                out_port = self.mac_to_port[self.switch[sw][DPID]][self.ip_to_mac[dst_ip]] 
                self.logger.info("  --- Output port set to %s" % (out_port))

                actions = [dp.ofproto_parser.OFPActionOutput(int(out_port))]

                data = msg.data
                pkt = packet.Packet(data)
                eth = pkt.get_protocol(ethernet.ethernet)
                #change the mac address of packet
                eth.dst = self.ip_to_mac[dst_ip]

                self.logger.info("  --- Changing destination mac to %s" % (eth.dst))

                pkt.serialize()

                out = dp.ofproto_parser.OFPPacketOut(
                    datapath=dp, buffer_id=0xffffffff, in_port=datapath.ofproto.OFPP_CONTROLLER,
                    actions=actions, data=pkt.data)
                print("---------")                
                dp.send_msg(out)
                return

	''' v3 '''
        # Learn MAC/PORT 
        if src not in self.mac_to_port:
            self.logger.info("  Learned MAC address %s on port %s",src,msg.in_port)
            self.mac_to_port[src] = msg.in_port

        ''' v4
        # Filtering
        if src in self.filter:
            self.logger.info("  MAC %s is filtered", src)
            return
        '''



        # Forward the packet 
        if dst in self.mac_to_port[str(dpid)]:
            out_port = self.mac_to_port[str(dpid)][dst]
            self.logger.info("  Destination MAC is on port %s. Forwarding the packet", out_port)
        else:
            out_port =  ofproto.OFPP_FLOOD
            self.logger.info("  Destination MAC not present in table. Flood the packet")


        actions = [datapath.ofproto_parser.OFPActionOutput(int(out_port))]

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=msg.in_port,
            actions=actions, data=data)
        datapath.send_msg(out)

        ''' v5 '''
        # Install flow
        if out_port != ofproto.OFPP_FLOOD:
            self.add_flow(datapath, msg.in_port, dst, actions)
            return


        ''' v2
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:  
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=msg.in_port,
            actions=actions, data=data)
        datapath.send_msg(out)
        '''
class LookupController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(LookupController, self).__init__(req, link, data, **config)
        self.lookup_api_app = data['lookup_api_app']

    @route('lookup', '/v1.0/lookup/lookup',
           methods=['GET'])
    def list_lookup(self, req, **kwargs):
        lookup_table = self.lookup_api_app.lookup
        body = json.dumps(lookup_table, sort_keys=True)
        return Response(content_type='application/json', body=body)

    
    @route('lookup', '/v1.0/lookup/switches',
           methods=['GET'])
    def list_switch(self, req, **kwargs):
        body = json.dumps(switch_table, sort_keys=True)
        return Response(content_type='application/json', body=body)


    @route('lookup', '/v1.0/lookup/bridge-table',
           methods=['GET'])
    def list_bridge_table(self, req, **kwargs):
        bridge_table = self.lookup_api_app.mac_to_port
        body = json.dumps(bridge_table, sort_keys=True)
        return Response(content_type='application/json', body=body)

    @route('lookup', '/v1.0/lookup/ip-to-mac',
           methods=['GET'])
    def list_ip_to_mac_table(self, req, **kwargs):
        ip_to_mac_table = self.lookup_api_app.ip_to_mac
        body = json.dumps(ip_to_mac_table, sort_keys=True)
        return Response(content_type='application/json', body=body)


