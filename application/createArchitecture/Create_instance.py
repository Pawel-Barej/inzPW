
from application.createArchitecture.Create_network import *
import openstack

conn = openstack.connect(cloud='openstack')

image_name = 'test_image'
name_instance = 'test1_new_instance'

def import_image(conn):
    print("Import Image:")

    # Url where glance can download the image
    uri = 'https://download.cirros-cloud.net/0.4.0/' \
          'cirros-0.4.0-x86_64-disk.img'

    # Build the image attributes and import the image.
    image_attrs = {
        'name': image_name,
        'disk_format': 'qcow2',
        'container_format': 'bare',
        'visibility': 'public',
    }
    image = conn.image.create_image(**image_attrs)
    conn.image.import_image(image,
                            method="website-download",
                            uri=uri)

def find_server(conn, name_server):
    #server = conn.compute.find_server("")
    for server in conn.compute.servers():
        if server.name == name_server:
            data_server = server

    return data_server


def create_server(conn):
    print("Create Server:")

    image = conn.compute.find_image(image_name)
    flavor = conn.compute.find_flavor('m1.tiny')
    network = conn.network.find_network(name_network)

    server = conn.compute.create_server(
        name='new-instance', image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": network.id}])

    server = conn.compute.wait_for_server(server)
    print(server)


def delete_server(conn, name_server):
    print("Delete server:")
    conn.compute.delete_server(find_server(conn, name_server))




