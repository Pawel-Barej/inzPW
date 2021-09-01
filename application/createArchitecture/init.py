from application.createArchitecture.Create_router import  *
from application.createArchitecture.Create_instance import *
from application.createArchitecture.Create_network import *

conn = openstack.connect(cloud='openstack')



def init(conn):

    create_network(conn)
    create_port(conn, name_port, name_network)
    create_router(conn)
    add_interface_to_router(conn)
    #import_image(conn)
    create_server(conn)
