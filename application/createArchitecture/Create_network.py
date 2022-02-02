import openstack

conn = openstack.connect(cloud='openstack')

name_network = 'example_new_network'
name_subnet = 'example_new_subnet'
name_port = 'example_new_port1'
name_external_network = 'external'
name_external_subnet = 'example_new_subnet'


# utworzenie sieci i podsieci
def create_network_with_subnets(conn, network_name, name_subnet, cidr, gateway_ip):
    print("Create Network:")

    new_network = conn.network.create_network(
        name=network_name)

    new_subnet = conn.network.create_subnet(
        name=name_subnet,
        network_id=new_network.id,
        ip_version='4',
        cidr=cidr,
        gateway_ip=gateway_ip,
        dns_nameservers=['8.8.8.8'],
        enable_dhcp=True)  # Jak coś nie działa to zaznacz że True

    print(new_subnet)


def find_network(conn, name_network):
    print("find network")
    for network in conn.network.networks():
        if network.name == name_network:
            data_network = network
            return data_network


def create_port(conn, name_port, name_network, name_subnet, ip_address):
    print("Create Port")

    new_port = conn.network.create_port(
        name=name_port,
        network_id=find_network(conn, name_network).id,
        fixed_ips=[{'subnet_id': find_subnet(conn, name_subnet).id, 'ip_address': ip_address}]
    )
    print(new_port)


# Lista podsieci
def find_subnet(conn, name_subnet):
    for subnet in conn.network.subnets():
        if subnet.name == name_subnet:
            subnet_internal_network = subnet
            return subnet_internal_network


def find_port(conn, name_port):
    for port in conn.network.ports():
        if port.name == name_port:
            data_port = port

            return data_port


def delete_network(conn, name_network, name_subnet):
    print("Delete network and subnet:")

    conn.network.delete_subnet(find_subnet(conn, name_subnet), ignore_missing=False)
    conn.network.delete_network(find_network(conn, name_network), ignore_missing=False)
