from application.website.control import *

import openstack


conn = openstack.connect(cloud='openstack')

def delete_architecture(conn):
    delete_server(conn, 'new-instance')
    remove_interface_from_router(conn, "example_router", "example_new_subnet", "example_new_port1")
    delete_router(conn, "example_router")
    delete_network(conn, 'example_new_network', 'example_new_subnet')
