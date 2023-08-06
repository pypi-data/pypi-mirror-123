#!/usr/bin/env python3
import sys, os, time, socket, re, copy
from netdevice import linux
import simplejson as json
import ipaddress
from binascii import hexlify, unhexlify
import random
try:
    # Python 2.
    from StringIO import StringIO
    # Python 3.
except ImportError:
    from io import StringIO

try:
    # Python 2.
    import urlparse
except ImportError:
    # Python 3.
    import urllib.parse as urlparse

ovstools_script = '''
#!/bin/bash
#Transfer the ip address from $bridge to $physicial interface.
# INPUT:
#     br: bridge name
#     ifname: interface name
# OUTPUT:
#     null
# sh .netdevice_ovstools.sh takeover eno1 br0 eno1
function ovsif_takeover()
{
    local ifname=$1
    local br=$2
    local port=$3
    local ip4=""
    local ip6=""
    #local mac=""
    local route=""

    ip4=$(ip -o -4 addr list $ifname | awk '{print $4}')
    # TODO:IPV6
    ip6=$(ip -o -6 addr list $ifname | awk '{print $4}')
    #mac=$(ip link show $ifname | grep "link/ether" | awk '{print $2}')
    IFS=$'
'
    route=($(ip route show | grep $ifname | grep -v link | sed "s/$ifname/$br/g"))

    echo "#Take over $ip4 from $ifname to $br($port)."
    ip addr flush dev $ifname
    echo "ip addr flush dev $ifname"

    # Add the physicial interface to the bridge $br
    ovs-vsctl --may-exist add-port $br $port
    echo "ovs-vsctl --may-exist add-port $br $port"

    #if [[ $ifname == $port ]]
    #then
    #    # Add the physicial interface to the bridge $br
    #    ovs-vsctl add-port $br $ifname
    #    echo "ovs-vsctl add-port $br $ifname"
    #fi

    #ovs-vsctl set bridge $br other_config:hwaddr=$mac
    ip link set $br up
    echo "ip link set $br up"
    if [ -n "$ip4" ]; then
        ip address add $ip4 dev $br
        echo "ip address add $ip4 dev $br"
    else
        echo "ip4 is empty, ignore..."
    fi

    # transfer the route from $ifname to $br
    for line in ${route[@]};
    do
        #echo "ip route add $line"
        eval ip route add $line
    done

    return 0
}

#Restore the ip address from $physicial interface to $bridge.
# INPUT:
#     br: bridge name
#     ifname: interface name
# OUTPUT:
#     null
function ovsif_restore()
{
    local ifname=$1
    local br=$2
    local port=$3
    local ip4=""
    local ip6=""
    local route=""

    ip4=$(ip -o -4 addr list $br | awk '{print $4}')
    # TODO:IPV6
    ip6=$(ip -o -6 addr list $br | awk '{print $4}')
    IFS=$'
'
    route=($(ip route show | grep $br | grep -v link | sed "s/$br/$ifname/g"))

    echo "#restore $ip4 from $br to $ifname, del $port from $br."
    ip addr flush dev $br
    echo "ip addr flush dev $br"
    ovs-vsctl del-port $br $port
    echo "ovs-vsctl del-port $br $port"
    ip address add $ip4 dev $ifname
    echo "ip address add $ip4 dev $ifname"
    
    # transfer the route from $ifname to $br
    for line in ${route[@]};
    do  
        #echo "ip route add $line"
        eval ip route add $line
    done
    
    return 0
}

function ovsif_help()
{
    echo "Usage:"
    echo "    sh $0 takeover br ifname."
    echo "    sh $0 restore br ifname."
}

# The main function for ovsif takeover
# INPUT: $@: All the parameters
# OUTPUT: null
# RETURN: 0 if succeed, or else
function main()
{
    local params=""

    if test $# -eq 0
    then
        ovsif_help
        return 0
    fi

    local pid_num_of_ovs=0
    pid_num_of_ovs=$(ps -ef | grep -w ovs-vswitchd | grep -v grep | wc -l)
    if test $pid_num_of_ovs -le 0
    then
        echo "It seems that OVS is not running. Please start it at first."
        return 0
    fi

    case "$1" in
        takeover)
            shift
            ovsif_takeover "$@" ;;
        restore)
            shift
            ovsif_restore "$@" ;;
        *)
            shift
            ovsif_help ;;
    esac
}

# Variables must be declared explicitly
set -u
main "$@"
exit $?

# vim: ts=4 sw=4 cindent expandtab
'''


class OvsHost(linux.LinuxDevice):
    '''
    OvsHost is a linux host with OpenvSwitch installed. You can build the
    topology and run test on it.

    Now it integerate the docker and can connect the container automatically.
    '''
    def __init__ (self, server = None, **kwargs):
        '''
        Connect the host and start the OVS.
        '''

        kwargs["type"] = 'OVS'
        linux.LinuxDevice.__init__(self, server, **kwargs)
        self.devices = []
        self.macs = []

        # start the docker if it's not running
        self.cmd('ovs-ctl start')
        self.cmd('systemctl start docker')

        cmd = "ls -l /sys/class/net/ | egrep -v 'virtual|total' | awk '{print $9}'"
        self.nics = self.cmd(cmd, log_level = 4).split()
        self.log("host's phicial nics: %s" %(self.nics))

        #vlog: 0: no change. 1: emer, 2: err, 3: warn, 4: info, 5: dbg, -1: off
        self["vlog"] = (self["vlog"]) and int(self["vlog"]) or 0
        if (self["vlog"] > 0):
            self.cmd('echo > /usr/local/var/log/openvswitch/ovs-vswitchd.log')
        #self.cmd('echo > /usr/local/var/log/openvswitch/ovsdb-server.log')
        if (self["vlog"] == -1):
            self.cmd('ovs-appctl vlog/set ANY:ANY:off')
        elif (self["vlog"] == 1):
            self.cmd('ovs-appctl vlog/set ANY:file:emer')
        elif (self["vlog"] == 2):
            self.cmd('ovs-appctl vlog/set ANY:file:err')
        elif (self["vlog"] == 3):
            self.cmd('ovs-appctl vlog/set ANY:file:warn')
        elif (self["vlog"] == 4):
            self.cmd('ovs-appctl vlog/set ANY:file:info')
        elif (self["vlog"] >= 5):
            self.cmd('ovs-appctl vlog/set ANY:file:dbg')
        #self.cmd('ovs-appctl vlog/list')

    def __del__(self):
        '''
        Get the trace file.
        Don't stop the OVS or docker.
        '''
        if (self["vlog"] > 0):
            #self.get_file('/usr/local/var/log/openvswitch/ovsdb-server.log',
            #        "%s_ovsdb-server.log" %(self["name"]))
            self.get_file('/usr/local/var/log/openvswitch/ovs-vswitchd.log',
                    "%s_ovs-vswitched.log" %(self["name"]))
        linux.LinuxDevice.__del__(self)

    def add_br (self, name, *args, **kwargs):
        '''
        Add a bridge and build the subnet.

        A bridge looks like this:

            vm1_vxlan0 = {"name": "vxlan0",
                           "type": "vxlan",
                           "options:remote_ip": "192.168.63.113",
                           "options:key": "flow" }
            vm1_br_int = {"name": "br-int",
                          "datapath_type": "netdev",
                          "port": [ vm1_vxlan0, ]}

        And devices look like this:

            con1 = {"name": "con1",
                    "type": "container",
                    "interface": "eth1",
                    "ip": "10.208.1.11/24"}

        '''
        ip = kwargs.pop("ip", []) #get the ip configuration of the bridge
        # Process the ports and bonds specially:
        ports = list(args)
        ports.extend(kwargs.pop("port", [])) # get the ports list
        bonds = kwargs.pop("bond", {}) # get the ports list
        # Create the kwargs
        command = 'ovs-vsctl --may-exist add-br %s' %(name)
        if kwargs:
            # If there is parameters, for example datapath_type, etc.
            command += ' -- set bridge %s' %(name)
            for k,v in kwargs.items():
                command += ' %s=%s' %(k,v)
                self[k] = v
        self.cmd(command) #execut the command.

        # delete the current offlow when it's created
        #if self["fail-mode"] == "secure":
        if self.cmd("ovs-vsctl get-fail-mode %s" %(name)).strip() == "secure":
            self.ofctl_add_flow(name, "priority=0,actions=drop")

        for p in ports:
            p["mac"] = self.add_port(name, **p)
        if bonds:
            self.add_bond(name, bonds["name"], *bonds["port"])

        if ip:
            # Configure the ip address for the address for route
            #for p in ports:
            #    self.cmd("ip addr flush dev %s" %(p["name"]))
            self.cmd('ip link set %s up' %(name))
            self.cmd('ip address add %s dev %s' %(ip, name))
            #self.cmd('ovs-appctl ovs/route/add %s %s' %(ip, name))

    def add_bond (self, bridge_name, bond_name, *args, **kwargs):
        '''
        Add bond.
        '''
        ip = kwargs.pop("ip", []) #ip is private paramater.
        for p in args:
            self.cmd("ip addr flush dev %s" %(p))
        cmd = "ovs-vsctl add-bond %s %s" %(bridge_name, bond_name)
        cmd += " " + " ".join(args)
        cmd += " " + " ".join('%s=%s' %(k,v) for k,v in kwargs.items())
        self.cmd(cmd)

        if ip:
            # Configure the ip address for the address for route
            self.cmd('ip link set %s up' %(bridge_name))
            self.cmd('ip address add %s dev %s' %(ip, bridge_name))

    def add_port (self, bridge_name, name, **kwargs):
        '''
        Add a port to the brige and do some configuration if necessary.
        return the mac address of the port if has.
        '''
        #if (kwargs.get("type", "normal") == "normal") and \
        #        (name in self.nics):
        #    #If it's a normal interface, take over it
        #    self.takeover_interface(name, bridge_name, name)
        #    return None

        command = 'ovs-vsctl --may-exist add-port %s %s' %(bridge_name, name)

        # parameter ip/mac is not valid, won't be included in the add-port
        port_options = {}
        for k,v in kwargs.items():
            if (k not in ["name", "ip", "mac"]):
                port_options[k] = v
        if port_options:
            command += ' -- set Interface %s' %(name)
            for k,v in port_options.items():
                command += ' %s=%s' %(k,v)
        self.cmd(command) #execut the command.

        macaddr = self.ovs_get_interface(name, "mac_in_use").strip('"')
        #kwargs["mac"] = macaddr
        self.macs.append(macaddr)
        if (kwargs.get("type", "normal") == "normal"):
            # For normal port, flush it and then set the ip if there is any.
            self.cmd("ip addr flush dev %s" %(name))
        if kwargs.get("ip", None) :
            # Configure the ip address for the address for route
            self.cmd('ip link set %s up' %(name))
            self.cmd('ip address add %s dev %s' %(kwargs["ip"], name))
            #self.cmd('ovs-appctl ovs/route/add %s %s' %(kwargs["ip"], name))
            #if self["fail-mode"] == "secure":
            if self.cmd("ovs-vsctl get-fail-mode %s" %(bridge_name)).strip() == "secure":
                # Confiure the default offlow for self port with IP.
                ipaddr = ipaddress.ip_interface(kwargs["ip"]).ip
                self.ofctl_add_flow(bridge_name,
                    'priority=10000,arp,arp_tpa=%s,arp_op=1,actions=move:"NXM_OF_ETH_SRC[]->NXM_OF_ETH_DST[]",mod_dl_src:"%s",load:"0x02->NXM_OF_ARP_OP[]",move:"NXM_NX_ARP_SHA[]->NXM_NX_ARP_THA[]",load:"0x%s->NXM_NX_ARP_SHA[]",move:"NXM_OF_ARP_SPA[]->NXM_OF_ARP_TPA[]",load:"0x%s->NXM_OF_ARP_SPA[]",in_port'%(ipaddr, macaddr, re.sub(r":", "", macaddr), "".join(f"{i:02x}" for i in ipaddr.packed)),
                    'priority=10000,icmp,nw_dst=%s,icmp_type=8,icmp_code=0,actions=push:"NXM_OF_ETH_SRC[]",push:"NXM_OF_ETH_DST[]",pop:"NXM_OF_ETH_SRC[]",pop:"NXM_OF_ETH_DST[]",push:"NXM_OF_IP_SRC[]",push:"NXM_OF_IP_DST[]",pop:"NXM_OF_IP_SRC[]",pop:"NXM_OF_IP_DST[]",load:"0xff->NXM_NX_IP_TTL[]",load:"0->NXM_OF_ICMP_TYPE[]",in_port' %(ipaddr),
                    )
        return macaddr

    def takeover_interface (self, ifname, bridge, port = None):
        '''
        takeover the ip from @ifname to @bridge(@port)
        '''
        filename = '.netdevice_ovstools.sh'
        if self.cmd("[ -f ~/%s ] || echo no" %(filename)).strip() == "no":
            with open(filename, 'w') as f:
                f.write(ovstools_script)
            self.put_file(filename, "~/")

        self.cmd("sh ~/%s takeover %s %s %s" %(filename,
            ifname, bridge, port and port or ifname))

    def no_takeover_interface (self, ifname, bridge, port = None):
        '''
        restore the ip from @bridge(@port) to @ifname
        '''
        filename = ".netdevice_ovstools.sh"
        if self.cmd("[ -f ~/%s ] || echo no" %(filename)).strip() == "no":
            with open(filename, 'w') as f:
                f.write(ovstools_script)
            self.put_file(filename, "~/")

        self.cmd("sh ~/%s restore %s %s %s" %(filename,
            ifname, bridge, port and port or ifname))

    def add_device (self, bridge_name, *args, **kwargs):
        '''
        connect devices to ovs, now only support container.
        '''
        # Add remote-device and it's peer self-port
        for arg in args:
            # allocate and add the device into the list

            dtype = arg.get("type", None)
            if dtype == "container":
                self.__add_container(bridge_name, **arg)

                macaddr = self.cmd(
                    "docker exec -it %s ip link show %s | grep link/ether"
                    %(arg["name"], arg["interface"]), log_level = 4)
                # be compatible with the old version.
                arg["mac"] = macaddr.split()[1]
                arg["ofport"] = self.ovs_get_container_ofport(arg["name"])
                self.macs.append(arg["mac"])
                self.devices.append(arg)

                # Configure offlow for the same subnet
                #if self["fail-mode"] == "secure":
                if self.cmd("ovs-vsctl get-fail-mode %s" %(bridge_name)).strip() == "secure":
                    ipaddr = ipaddress.ip_interface(arg["ip"])
                    self.ofctl_add_flow(bridge_name,
                        "priority=10000,arp,arp_tpa=%s,actions=output:%s"
                        %(ipaddr.ip, arg["ofport"]),
                        # We always know the mac/port mapping, so add it.
                        "priority=10001,dl_dst=%s,actions=output:%s" 
                        %(arg["mac"], arg["ofport"]),
                        )
            elif dtype == "vm":
                self.__add_vm(bridge_name, arg)
            else:
                self.log("device type %s is not supported now..." %(dtype))

    def __add_container (self, bridge_name,
            name = "con1",
            host_dir = "/var/shared",
            container_dir = "/var/shared", 
            interface = "eth1",
            **kwargs):
        '''
        Create a container and connect it to the bridge: bridge_name.
        '''
        #创建容器, 设置net=none可以防止docker0默认网桥影响连通性测试
        self.cmd('docker run --privileged -d --name %s --net=none -v %s:%s -it centos'
                %(name, host_dir, container_dir))
        #self.cmd(' docker exec -it con11 rpm -ivh /var/shared/tcpdump-4.9.3-1.el8.x86_64.rpm ')


        cmd = 'ovs-docker add-port %s %s %s' %(bridge_name, interface, name)
        if (kwargs.get("ip", None)):
            cmd += " --ipaddress=%s" %(kwargs["ip"])
        if (kwargs.get("mac", None)):
            cmd += " --macaddress=%s" %(kwargs["mac"])
        if (kwargs.get("gateway", None)):
            cmd += " --gateway=%s" %(kwargs["gateway"])
        if (kwargs.get("mtu", None)):
            cmd += " --mtu=%s" %(kwargs["mtu"])
        self.cmd(cmd)

        # Configure vlan on self-port if the device has vlan configured.
        if (kwargs.get("vlan", None)):
            self.cmd('ovs-vsctl set port %s tag=%d'
                    %(ovs_get_container_port(bridge_name, name = name),
                        kwargs["vlan"]))

    def __add_vm (self, bridge_name, vm):
        '''
        # The following parameter are mandatory:
        vm11 = {"name": "vm11", "type": "vm", "password": "sangfor",
                "-hda": "/media/qemu/vm1_CentOS8.img",
                "-vnc": ":11",
                "-smp": "sockets=1,cores=1",
                "-m": "4096M",
                "port": [vm11_port0, vm11_port1]}
        '''

        vm["-name"] = vm.get("-name", vm.get("name", "tmp"))
        vm["-cpu"] = vm.get("-cpu", "host")
        vm["-m"] = vm.get("-m", "2048M")
        vm["-smp"] = vm.get("-smp", "sockets=1,cores=1")
        vm["-boot"] = vm.get("-boot", "c")
        vm["-pidfile"] = vm.get("-pidfile",
                "/tmp/%s.pid" %(vm["-name"]))
        vm["-enable-kvm"] = vm.get("-enable-kvm", "")
        vm["-object"] = vm.get("-object",
            "memory-backend-file,id=mem,size=%s,mem-path=/dev/hugepages,share=on"
            %(vm["-m"]))
        vm["-numa"] = vm.get("-numa", "node,memdev=mem")
        vm["-mem-prealloc"] = vm.get("-mem-prealloc", "")

        cmd = vm.get("mask", None) and ("taskset %s " %(vm["mask"])) or ""
        cmd += "qemu-system-x86_64"
        for k,v in vm.items():
            if k[0] == "-":
                cmd += ' %s %s' %(k,v)
        for p in vm.get("port", []):
            for k,v in p.items():
                if k[0] == "-":
                    #bypass the parameters: name, ip
                    cmd += ' %s %s' %(k,v)

        # 1) Add vhostuser port
        for p in vm.get("port", []):
            #self.log("__add_vm(), p: %s" %(p))
            #device = self._util_dictionary_parse(p["-device"].split(","))
            if p.get("-netdev", None) and "vhost-user" in p["-netdev"]:
                chardev = self._util_dictionary_parse(p["-chardev"].split(","))
                if ("server" in chardev):
                    # vhostuserclient
                    port_name = os.path.basename(chardev["path"])
                    ovs_port = {"name": port_name,
                            "type": "dpdkvhostuserclient",
                            "options:vhost-server-path": chardev["path"]}
                else:
                    # type: vhostuser
                    port_name = os.path.basename(chardev["path"])
                    ovs_port = {"name": port_name, "type": "dpdkvhostuser"}
                ovs_port["mac"] = self.add_port(bridge_name, **ovs_port)

        # 2)start the qemu: tap mode need to start the qemu at frist,
        # vhostuser need to start the ovs-port at first. 
        tmp = self.cmd("%s -daemonize" %(cmd))
        #self.log("%s -daemonize" %(cmd))

        # 3)add the tap port, and add the flow
        for p in vm.get("port", []):
            #self.log("__add_vm(), p: %s" %(p))
            device = self._util_dictionary_parse(p["-device"].split(","))
            if (device["type"] == "virtio-net-pci" and p.get("-netdev", None)):
                netdev = self._util_dictionary_parse(p["-netdev"].split(","))
            else:
                self.log("OVS doesn't support device: %s." %(device["type"]))
                continue

            if "vhost-user" in p["-netdev"]:
                br = bridge_name
                pass
            elif "tap" in p["-netdev"]:
                # type: tap
                #netdev = self._util_dictionary_parse(p["-netdev"].split(","))
                port_name = netdev.get("ifname", netdev.get("id", "id0"))
                ovs_port = {"name": port_name}
                br = netdev.get("br", "br0") #default=br0
                if (netdev.get("script", "/etc/qemu-ifup") == "no"):
                    # There is no user-defined script, we add it by ourselves:
                    self.cmd("ip link set %s up" %(port_name))
                    ovs_port["mac"] = self.add_port(br, **ovs_port)
            elif "bridge" in p["-netdev"]:
                # type: tap
                #netdev = self._util_dictionary_parse(p["-netdev"].split(","))
                port_name = "%s_%s" %(vm["-name"], netdev.get("id", "tmp"))
                ovs_port = {"name": port_name}
                br = netdev.get("br", "br0") #default=br0
                # qemu would add the port automatically for tap interface.
                self.cmd("ip link set %s up" %(port_name))
                ovs_port["mac"] = self.add_port(br, **ovs_port) #default=br0
            else:
                # Now only vhost-user and tap will be added into OVS
                continue

            p["mac"] = device["mac"] # Record the mac for use later
            p["ofport"] = self.ovs_get_interface(port_name, "ofport")
            self.macs.append(p["mac"])
            self.devices.append(p)

            # Configure offlow for the same subnet
            #if self["fail-mode"] == "secure":
            if self.cmd("ovs-vsctl get-fail-mode %s" %(br)).strip() == "secure":
                ipaddr = ipaddress.ip_interface(p["ip"])
                self.ofctl_add_flow(br,
                    "priority=10000,arp,arp_tpa=%s,actions=output:%s"
                    %(ipaddr.ip, p["ofport"]),
                    # We always know the mac/port mapping, so add it.
                    "priority=10001,dl_dst=%s,actions=output:%s" 
                    %(p["mac"], p["ofport"]),
                    )

    def add_vtep (self, bridge_name, vtep, *args):
        '''
        Add some flows remote devices(*args): 从本主机上到达所有*args的包，全
        部经由vtep
        '''
        #if self["fail-mode"] != "secure":
        if self.cmd("ovs-vsctl get-fail-mode %s" %(bridge_name)).strip() != "secure":
            #Don't need configure vtep explicitly in standalone mode.
            return

        str_vtep = (isinstance(vtep, dict)) and vtep["name"] or vtep
        vxlan_ofport = self.ovs_get_interface(str_vtep, "ofport")
        for arg in args:
            str_ip = (isinstance(arg, dict)) and arg["ip"] or arg
            ipaddr = ipaddress.ip_interface(str_ip).ip
            self.ofctl_add_flow(bridge_name,
                    "priority=1000,arp,arp_tpa=%s,actions=output:%s"
                    %(ipaddr, vxlan_ofport),
                    "priority=1000,ip,nw_dst=%s,actions=output:%s" 
                    %(ipaddr, vxlan_ofport))

    def add_gateway (self, bridge_name, gw, *args):
        '''
        Add some flows to ofproto
        '''
        #if self["fail-mode"] != "secure":
        if self.cmd("ovs-vsctl get-fail-mode %s" %(bridge_name)).strip() != "secure":
            #Don't need configure gateway explicitly in standalone mode.
            return

        #self.log("gw mac: %s" %(gw["mac"]))
        #self.log("mac: %s" %(self.macs))
        if (gw["mac"] not in self.macs):
            # gw is not on this node, Add it as if it's on this node.
            ipaddr = ipaddress.ip_interface(gw["ip"]).ip
            self.ofctl_add_flow(bridge_name,
                    'priority=1000,arp,arp_tpa=%s,arp_op=1,actions=move:"NXM_OF_ETH_SRC[]->NXM_OF_ETH_DST[]",mod_dl_src:"%s",load:"0x02->NXM_OF_ARP_OP[]",move:"NXM_NX_ARP_SHA[]->NXM_NX_ARP_THA[]",load:"0x%s->NXM_NX_ARP_SHA[]",move:"NXM_OF_ARP_SPA[]->NXM_OF_ARP_TPA[]",load:"0x%s->NXM_OF_ARP_SPA[]",in_port'%(ipaddr,
                        gw["mac"],
                        re.sub(r":", "", gw["mac"]),
                        "".join(f"{i:02x}" for i in ipaddr.packed)),
                    'priority=1000,icmp,nw_dst=%s,icmp_type=8,icmp_code=0,actions=push:"NXM_OF_ETH_SRC[]",push:"NXM_OF_ETH_DST[]",pop:"NXM_OF_ETH_SRC[]",pop:"NXM_OF_ETH_DST[]",push:"NXM_OF_IP_SRC[]",push:"NXM_OF_IP_DST[]",pop:"NXM_OF_IP_SRC[]",pop:"NXM_OF_IP_DST[]",load:"0xff->NXM_NX_IP_TTL[]",load:"0->NXM_OF_ICMP_TYPE[]",in_port' %(ipaddr))

        for d in args:
            #self.log("d: %s" %(d))
            if d.get("mac", None) and (d['mac'] in self.macs):
                #self.log("d: %s" %(d))
                # ONly change the mac and ttl on the same host.
                self.ofctl_add_flow(bridge_name,
                    "priority=1000,ip,nw_dst=%s,action=mod_dl_src:%s,"
                    "mod_dl_dst:%s,dec_ttl,output:%s"
                    %(d["ip"].split("/")[0], gw["mac"], d["mac"], d["ofport"]))

    def set_out_interface (self, bridge_name, out_if, *args):
        '''
        It's the same as add_vtep(), only different in the name.
        '''
        #if self["fail-mode"] != "secure":
        if self.cmd("ovs-vsctl get-fail-mode %s" %(bridge_name)).strip() != "secure":
            #Don't need configure out_if explicitly in standalone mode.
            return
        for arg in args:
            ipaddr = ipaddress.ip_interface(arg["ip"]).ip
            vxlan_port = self.ovs_get_interface(out_if["name"], "ofport")
            self.ofctl_add_flow(bridge_name,
                    "priority=1000,arp,arp_tpa=%s,actions=output:%s"
                    %(ipaddr, vxlan_port),
                    "priority=1000,ip,nw_dst=%s,actions=output:%s" 
                    %(ipaddr, vxlan_port))

    def del_br (self, *args, **kwargs):
        '''
        Delete the bridge and all the connected devices(containers).

        If bridge name is not given, delete all the bridges.
        '''
        # delete all the bridges in the OVS
        bridges = args and args or self.cmd("ovs-vsctl list-br")
        for b in StringIO(bridges).readlines():
            b = b.strip()
            ports = self.cmd("ovs-vsctl list-ports %s" %(b))
            for p in StringIO(ports).readlines():
                # delete all the devices(container/vm/physical) connectting to.
                p = p.strip()
                external_ids = self.ovs_get_interface(p, "external_ids")
                external_ids = external_ids.strip("{} \t\r\n")

                #self.log("debug, bridge: %s, port: %s" %(b, p))
                if (p in self.nics):
                    # Restore the "phisical" interface
                    self.no_takeover_interface(p, b, p)
                elif ("=" in external_ids):
                    # Parse external_ids: {container_id=con13, container_iface=eth1}
                    i = {}
                    for a in external_ids.split(",", 1):
                        k,v = a.split("=", 1)
                        i[k.strip()] = v.strip()
                    if (i.get("container_id", None)):
                        self.cmd('docker stop %s' %(i["container_id"]))
                        self.cmd('docker rm %s' %(i["container_id"]))
            self.cmd("ovs-vsctl del-br %s" %(b))
        self.cmd('ovs-vsctl show')
        #self.cmd('ovs-ctl stop')

    def ovs_get_interface (self, interface, attribute = None):
        '''
        Get a self-port which connect to the kwargs["name"]
        '''

        if attribute:
            result = self.cmd("ovs-vsctl get interface %s %s"
                    %(interface, attribute))
            return result.strip()

        i = {}
        result = self.cmd("ovs-vsctl list interface %s" %(interface),
                log_level=4)
        for p in StringIO(result).readlines():
            k,v = p.split(":", 1)
            i[k.strip()] = v.strip()

        #return attribute and i.get(attribute, None) or i
        return i

    def ovs_get_container_ofport (self, name, **kwargs):
        '''
        Get a self-port which connect to the kwargs["name"]
        '''

        bridges = self.cmd("ovs-vsctl list-br", log_level=4)
        for b in StringIO(bridges).readlines():
            ports = self.cmd("ovs-vsctl list-ports %s" %(b.strip()), log_level=4)
            for p in StringIO(ports).readlines():
                i = self.ovs_get_interface(p.strip())
                if (name in i.get("external_ids", None)):
                    return i.get("ofport", None)
        return None

    def ovs_get_container_port (self, name, **kwargs):
        '''
        Get a self-port which connect to the kwargs["name"]
        '''

        bridges = self.cmd("ovs-vsctl list-br", log_level=4)
        for b in StringIO(bridges).readlines():
            ports = self.cmd("ovs-vsctl list-ports %s" %(b.strip()), log_level=4)
            for p in StringIO(ports).readlines():
                i = self.ovs_get_interface(p.strip())
                if (name in i.get("external_ids", None)):
                    return i.get("name", None)
        return None

    def ofctl_add_flow (self, bridge_name, *args, **kwargs):
        '''
        Add some flows to ofproto
        '''
        for table in args:
            table = filter(lambda x: (x.strip()) and (x.strip()[0] != '#'),
                    StringIO(table.strip()).readlines())
            for l in table:
                # remove the line starting with '#'
                l = l.strip()
                if l[0] !=  "#":
                    self.cmd('ovs-ofctl add-flow %s %s' %(bridge_name, l))
        return None

    def ping_test (self, src, *args, **kwargs):
        '''
        Add some flows to ofproto
        '''
        for dst in args:
            dstip = ipaddress.ip_interface(dst["ip"])
            if src["type"] == "container":
                srcip = ipaddress.ip_interface(src["ip"])
                result = self.cmd('docker exec -it %s ping %s -c 1'
                        %(src["name"], dstip.ip))
            elif src["type"] == "vm":
                srcip = ipaddress.ip_interface(src["port"][1]["ip"])
                u = urlparse.urlparse(src["url"])

                if (u.password):
                    result = self.cmd('sshpass -p %s ssh %s@%s ping -c 1 %s'
                        %(u.password, u.username, u.hostname, dstip.ip))
                else:
                    # Maybe it doesn't need password
                    result = self.cmd('ssh %s@%s ping -c 1 %s'
                        %(u.username, u.hostname, dstip.ip))
            else:
                self.log("ERROR: don't support the type %s!"
                        %(src["type"]), bg_color = "purple")
                return False

            if "received, 0% packet loss," in result:
                self.log("PASS: %s ping %s, %s -> %s!" %(src["name"], dst["name"],
                    srcip.ip, dstip.ip), bg_color = "green")
            else:
                self.log("FAIL: %s ping %s, %s -> %s!" %(src["name"], dst["name"],
                    srcip.ip, dstip.ip), bg_color = "red")

    def _util_dictionary_parse (self, params):
        '''
        Add some flows to ofproto
        '''
        my_dic = {}
        if "=" not in params[0]:
            my_dic["type"] = params.pop(0)
        for attribute in params:
            if ("=" in attribute):
                k,v = attribute.split("=", 1)
                my_dic[k.strip()] = v.strip()
            else:
                my_dic[attribute] = ""
        return my_dic

    def vm_init (self, *args, gateways = [], script = None):
        '''
        Given some devivces and gates, caculate the route and configure route
        automatically.

        @args: The list of vm, the vm is a dictionary, it at least has the
        following part:

            vm11 = {'name': 'vm11',
            'url': 'ssh://root:sangfor@10.103.166.36',
            'port': [{'name': 'ens3', 'ip': '10.103.166.36'},
                {'name': 'ens4', 'ip': '10.208.1.11'}]}

        @gateways: The list of gateway. The gateway is a dictionary, it at
        least has the following part:

            gw1 = {"name": "gw1", "ip": "10.208.1.1/24"}

        @script: the script to run when login the rm.

        An example:

            host.vm_init(*devices, gateways = [gw1, gw2]) # configure route
        '''

        devices = copy.deepcopy(args)
        #subnets = (ipaddress.ip_interface(gw["ip"]).network for gw in gateways)
        for vm in devices:
            # Find via for every devices
            vm["ipaddress"] = ipaddress.ip_interface(vm["port"][1]["ip"]).ip
            for gw in gateways:
                #self.log("gw: %s, %s!" %(ipaddress.ip_interface(gw["ip"]).ip,
                #    ipaddress.ip_interface(gw["ip"]).network))
                if vm["ipaddress"] in ipaddress.ip_interface(gw["ip"]).network:
                    vm["via"] = ipaddress.ip_interface(gw["ip"]).ip

        for vm in devices:
            # Configure the route
            u = urlparse.urlparse(vm["url"])
            if script:
                self.cmd("sshpass -p %s scp %s %s@%s:~/" %(u.password, script,
                    u.username, u.hostname))
            c = script and ("sh ~/%s; " %(script)) or ""

            for gw in gateways:
                gw_ipaddress = ipaddress.ip_interface(gw["ip"])
                #self.log("gw: %s, %s!" %(gw_ipaddress.ip, gw_ipaddress.network))
                if vm["ipaddress"] not in gw_ipaddress.network:
                    c += "ip route add %s via %s dev %s" \
                            %(gw_ipaddress.network, vm["via"],
                                    vm["port"][1]["name"])
                    #self.log("%s, route: c: %s" %(vm["name"], c))

            self.cmd('sshpass -p %s ssh %s@%s "%s"' %(u.password,
                u.username, u.hostname, c))

    def vm_uninit (self, *args):
        '''
        Power off the virtual machine from this host.
        从这台主机上将给定的虚拟机关机。

        @args: The list of the vm to power on. Itis a dictionary and at least
        has the following part:
        @args: 需要关机的虚拟机列表。虚拟机用字典定义，应该至少具有下面的成员
        ：

            vm11 = {'url': 'ssh://root:sangfor@10.103.166.36'}

        An example:
        一个调用的例子：

            h1.vm_uninit(*devices)
        '''
        for vm in args:
            u = urlparse.urlparse(vm["url"])
            self.cmd('sshpass -p %s ssh %s@%s shutdown now' %(u.password,
                u.username, u.hostname))


if __name__ == '__main__':
    '''
    #topology：
        (vr1)vrl1 -- vsl1(dvs1)vsl1 -- vrl1(vr1)
    '''

    vm1 = OvsHost("ssh://root:sangfor@172.93.63.111", name = "vm1",
            log_color = "red", log_level = options.log_level)
    vm1_br_int = {"name": "br-int", "datapath_type": "netdev",
            "port": [ {"name": "vxlan0", "type": "vxlan",
                "options:remote_ip": "192.168.63.113", "options:key": "flow" }]}
    vm1_br_phy = {"name": "br-phy", "datapath_type": "netdev",
            "other_config:hwaddr": "fe:fc:fe:b1:1d:0b",
            }
    vm1_eth1 = {"name": "eth1", "type": "phy", "ip": "192.168.63.111/16"}
    con = []
    for i in range(4):
        con.append({"name": "con%d"%(i), "type": "container", "interface": "eth1",
            "ip": "10.208.1.%d/24" %(10+i)})
    vm1.log("container: %s\n" %(json.dumps(con, indent=4)))
    vm1.cmd('ovs-vsctl show')

    vm1.ovs_connect(vm1_br_int, con[0], con[1])
    vm1.ovs_connect(vm1_br_phy, vm1_eth1)
    vm1.cmd('ovs-vsctl show')

