from mininet.cli import CLI
from mininet.link import Link
from mininet.net import Mininet


def main():
    network = Mininet()

    # Add Host
    h1 = network.addHost("h1")
    h2 = network.addHost("h2")
    h3 = network.addHost("h3")
    h4 = network.addHost("h4")

    # Add L2 Switch
    s5 = network.addHost("s5")

    # Add link between host(s) and switch
    Link(h1, s5)
    Link(h2, s5)
    Link(h3, s5)
    Link(h4, s5)

    network.build()

    # Remove default IP addresses from host's interfaces
    h1.cmd("ifconfig h1-eth0 0")
    h2.cmd("ifconfig h2-eth0 0")
    h3.cmd("ifconfig h3-eth0 0")
    h4.cmd("ifconfig h4-eth0 0")

    # Remove default IP addresses from switch's interfaces
    s5.cmd("ifconfig s5-eth0 0")
    s5.cmd("ifconfig s5-eth1 0")
    s5.cmd("ifconfig s5-eth2 0")
    s5.cmd("ifconfig s5-eth3 0")

    # Create a VLAN 10 and VLAN 20 on Switch s5
    # Bring up the Vlan interfaces on L2 switch uo
    s5.cmd("brctl addbr vlan10")
    s5.cmd("brctl addbr vlan20")
    s5.cmd("ifconfig vlan10 up")
    s5.cmd("ifconfig vlan20 up")

    # Add s5-eth0, s5-eth.. to VLAN 10 on and VLAN 20 L2 switch in Access Mode
    s5.cmd("brctl addif vlan10 s5-eth0")
    s5.cmd("brctl addif vlan10 s5-eth1")
    s5.cmd("brctl addif vlan20 s5-eth2")
    s5.cmd("brctl addif vlan20 s5-eth3")

    h1.cmd("ifconfig h1-eth0 10.0.10.1 netmask 255.255.255.0")
    h2.cmd("ifconfig h2-eth0 10.0.10.2 netmask 255.255.255.0")
    h3.cmd("ifconfig h3-eth0 10.0.20.1 netmask 255.255.255.0")
    h4.cmd("ifconfig h4-eth0 10.0.20.2 netmask 255.255.255.0")

    h1.cmd("ip route add default via 10.0.10.254 dev h1-eth0")
    h2.cmd("ip route add default via 10.0.10.254 dev h2-eth0")
    h3.cmd("ip route add default via 10.0.20.254 dev h3-eth0")
    h4.cmd("ip route add default via 10.0.20.254 dev h4-eth0")

    CLI(network)

    network.stop()


if __name__ == '__main__':
    main()
