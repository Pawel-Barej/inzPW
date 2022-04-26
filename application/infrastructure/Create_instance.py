import openstack

from application.infrastructure.Create_network import find_network

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


def create_image(conn, name, data, disk_format):
    print("Upload Image:")

    # Build the image attributes and upload the image.
    image_attrs = {
        'name': name,
        'data': data,
        'disk_format': disk_format,
        'visibility': 'private',
    }
    conn.image.create_image(**image_attrs)


def find_server(conn, name_server):
    server = conn.compute.find_server(name_server)
    for server in conn.compute.servers():
        if server.name == name_server:
            data_server = server

    return data_server


def create_server(conn, image_name, name_network, name):
    print("Create Server:")

    image = conn.compute.find_image(image_name)
    flavor = conn.compute.find_flavor('m1.medium')
    network = conn.network.find_network(name_network)

    server = conn.compute.create_server(
        name=name,
        image_id=image.id,
        flavor_id=flavor.id,
        networks=[{"uuid": network.id}])
        #userdata="#!/bin/bash \n echo 'AMAZING TEST' > /root/test")

    server = conn.compute.wait_for_server(server)
    print(server)


def delete_server(conn, name_server):
    print("Delete website:")
    print(find_server(conn, name_server))
    conn.compute.delete_server(find_server(conn, name_server))


def delete_image(conn, image_name):
    print("Delete Image:")

    image = conn.image.find_image(image_name)

    conn.image.delete_image(image, ignore_missing=False)


def list_servers(conn):
    print("List Servers:")

    for server in conn.compute.servers():
        print(server)


def add_floating_ip_to_server(conn, name_server, address):
    conn.compute.add_floating_ip_to_server(find_server(conn, name_server).id, address, fixed_address=None)


def create_ip(conn):
    if conn.network.find_available_ip() == None:
        floating_ip = conn.network.create_ip(floating_network_id=find_network(conn, "external").id)

    else:
        floating_ip = conn.network.find_available_ip()

    return floating_ip.name
