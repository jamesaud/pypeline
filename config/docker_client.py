import os
import threading
import docker.tls as tls
from docker import Client
from config import config

CERTS = os.path.join(os.path.expanduser('~'), '.docker', 'machine', 'machines', 'default')
docker_machine_ip = '192.168.99.100'
tls_config = tls.TLSConfig(
    client_cert=(os.path.join(CERTS, 'cert.pem'), os.path.join(CERTS,'key.pem')),
    ca_cert=os.path.join(CERTS, 'ca.pem'),
    verify=True
)
cli = Client(base_url='https://{}:2376'.format(docker_machine_ip), tls=tls_config)
threads = [] # Threaded so printing doesn't wait for docker containers to finish running


def threaded(function):
    def wrapper(arg):
        t = threading.Thread(target=function,  args=(arg,))
        threads.append(t)
        t.start()
    return wrapper


@threaded
def print_threaded_generator(generator, process_name=''):  # Description name for the thread.
    for line in generator:
        print(line)


def pull(image_name):
    for line in cli.pull(image_name, stream=True):
        print(line)


# Find by image id
def find_image(image_id):
    return cli.inspect_image(image_id)


def find_image_by_name(image_name):
    return cli.images(image_name)


def find_container(container_id):
    return cli.inspect_container(container_id)


def remove_image(image): #id or name
    cli.remove_image(image, True)
    print("Removed image:", image)


def remove_container(container):
    cli.remove_container(container, True)
    print("Removed container :", container)


def build(dockerfile_path, image_name):
    print("Building image", image_name)
    print(os.listdir(os.getcwd()))
    logs_generator = cli.build(path=dockerfile_path, rm=True, tag=image_name)
    for line in logs_generator:
        print(line)


def push(push_url):
    for line in cli.push(push_url, stream=True):
        print(line)


def tag(image_id, repo, tag):
    tagged = repo + ":" + tag
    cli.tag(image_id, repo, tag)
    print('Tagged', image_id, tag)
    return tagged


# Returns container id
# -> str
def run_container(image, container_name, args): # Image: name or id
    container = cli.create_container(image=image, name=container_name, detach=True, command=args) # args can be a string or list
    container_id = container['Id']  # Get id from dictionary
    cli.start(container_id)  # Start the container
    print('Started container:', container_name, 'with commands:', "'{}'".format(args))
    #THIS LINE IS CAUSING ISSUES BECAUSE THE FOLLOWING .INSIDE COMMANDS WONT BE RUN BECAUSE IT WAITS FOR THE FIRST CONTAINER COMMAND TO FINISH
    print_threaded_generator(cli.logs(container=container_id, stdout=True, stream=True))  # Output logs in real time
    return container_id


def remove_container(container):
    cli.stop(container=container)
    cli.remove_container(container=container, v=True) # v=True means force remove
    print('Removed container:', container)


def inside_container(container_id, args):
    executor = cli.exec_create(container=container_id, cmd=args)
    exec_id = executor['Id']
    logs_generator = cli.exec_start(exec_id=exec_id, stream=True, detach=True)
    print_threaded_generator(logs_generator)
    print('Ran inside container:', container_id, 'with commands:', "'{}'".format(args))


