
from application.createArchitecture.Create_network import *
import openstack

conn = openstack.connect(cloud='openstack')
router_name = 'example_router'
name_subnet_public1 = 'public1-subnet'

def find_router(conn, name_router):
    for router in conn.network.routers():
        if router.name == name_router:
            data_router = router


    return data_router

def create_router(conn):
    print("Create router")

    new_router = conn.network.create_router(
        name = router_name,
        external_gateway_info={'network_id': find_network(conn, name_external_network).id,
                               'external_fixed_ips': [{'subnet_id': find_subnet(conn, name_subnet_public1).id}],
                               'enable_snat': True}
    )
    print(new_router)


def add_interface_to_router(conn):
    conn.network.add_interface_to_router(
       router = conn.network.find_router(router_name),
       subnet_id = find_subnet(conn, name_subnet).id,
       port_id = find_port(conn, name_port).id

   )


def remove_interface_from_router(conn, router_name, name_subnet, name_port):
    print("Delete interface from router")
    conn.network.remove_interface_from_router(
        router=conn.network.find_router(router_name),
        subnet_id=find_subnet(conn, name_subnet).id,
        port_id=find_port(conn, name_port).id
    )


def delete_router(conn, name_router):
    print("Delete router")
    conn.network.delete_router(find_router(conn, name_router))

