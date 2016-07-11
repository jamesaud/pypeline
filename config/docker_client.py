import docker
import os

cli = docker.from_env(assert_hostname=False)


def format_decorator(function): #Place on any function that prints, for better output formatting
    def called(*args, **kargs):
        print('\n')
        return function(*args, **kargs)
    return called


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
    for line in cli.build(path=dockerfile_path, rm=True, tag=image_name):
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
    container = cli.create_container(image=image, name=container_name, detach=True, command=args)
    container_id = container['Id']  # Get id from dictionary
    cli.start(container_id)  # Start the container
    print('Started container:', container_name, 'with commands:', "'{}'".format(args))
    for line in cli.logs(container=container_id, stdout=True, stream=True, timestamps=True):  # Output logs in real time
        print(line)
    return container_id


def remove_container(container):
    cli.stop(container=container)
    cli.remove_container(container=container, v=True) # v=True means force remove
    print('Removed container:', container)


def inside_container(container, args):
    cli.exec_create(container=container, cmd=args)
    for line in cli.logs(container=container, stdout=True, stream=True):
        print(line)
    print('Running inside container:', container, 'with commands:', "'{}'".format(args))
