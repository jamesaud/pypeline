import threading
import logging
from .config import DOCKER_CLIENT as cli

"""
The functions in this file are wrappers over the dockerpy api, an api for communicating directly with the docker client.
This is to keep consistency for all interactions with the docker api, and allow for package wide modifications.

It is required for some functions to be threaded...
Example: Printing real-time output from a container.
Problem - If you run a container, print the stdout in real time, and then exec into the container to run more commands,
          the printing prevents any more commands to be run until it is done. Therefore, exec won't run until the
          container stops running.
Solution - Assign background printing to a thread when the container is started.
Notes - Don't thread any printing function. For example, threading the build function is bad because it will run
        following commands before the image is done building!
References - Refer to  'https://github.com/docker/docker-py/blob/master/docs/api.md'  for the docker-py api
"""

threads = []  # Threads running. Refer to description above. IDK if this is correct.

def threaded(function):
    """
    Decorator that threads a function of one argument
    :param: Function - the function to wrap.
    :return: Function - a wrapped version of the passed function that runs threaded.
    """
    def wrapper(arg):
        t = threading.Thread(target=function,  args=(arg,))
        threads.append(t)
        t.start()
    return wrapper


def print_generator(generator):
    """
    Prints line by line from a generator, but makes it threaded.
    :param generator: Generator - The generator to print.
    :return: None
    """
    for line in generator:
        logging.info(line)


@threaded
def print_threaded_generator(generator):  # Description name for the thread.
    """
    Prints line by line from a generator, but makes it threaded.
    :param generator: Generator - The generator to print.
    :return: None
    """
    print_generator(generator)


# Improve - should have option for registry and login credentials.
def pull(image_name):
    """
    Pull image from registry, defaults to dockerhub.com.
    :param image_name: Str - the name of the image to pull.
    :return: None
    """
    generator = cli.pull(image_name, stream=True)
    print_generator(generator)


# Find by image id
def find_image(image_id):
    """
    Find image by id.
    :param image_id: Str - the id of the image to find.
    :return: Dict - a dictionary containing details about the image.
    """
    return cli.inspect_image(image_id)


def find_image_by_name(image_name):
    """
    Find image by name.
    :param image_name: Str - the name of the image to search for.
    :return: List - a list containing a dictionary containing details about the image...IDK why the api works like that.
    """
    return cli.images(image_name)


def find_container(container_id):
    """
    Find the container by id.
    :param container_id: Str - the id of the container to search for.
    :return: Dict - a dictionary containing details about the container.
    """
    return cli.inspect_container(container_id)


def remove_image(image):
    """
    Remove the image.
    :param image: Str - the id or name of the image.
    :return: None
    """
    cli.remove_image(image, True)
    logging.info("Removed image: " + image)


def remove_container(container):
    """
    Kill and delete the container
    :param container: Str - id or name of the container.
    :return: None
    """
    cli.remove_container(container, True)
    logging.info("Removed container : " + container)


def build(dockerfile_path, image_name):
    """
    Build image from dockerfile in specified path.
    :param dockerfile_path: Str - full path of the dockerfile.
    :param image_name: Str - name to give the image.
    :return: None
    """
    logging.info("Building image " + image_name)
    logs_generator = cli.build(path=dockerfile_path, rm=True, tag=image_name)
    for line in logs_generator:
        logging.info(line)


# Improve - should be able to give repository login credentials.
def push(image_name):
    """
    Push image to repository.
    :param push_name: the name of the image to push.
    :return: None
    """
    for line in cli.push(image_name, stream=True):
        logging.info(line)


# Improve - use the docker api to get the actual tag of the image, not creating it with by hand. Might run into errors
#           where it is not the same as the actual name.
def tag(image_id, repo, tagged):
    """
    Re-Tag an image. Same as 'docker tag image tagName'
    :param image_id:
    :param repo:
    :param tag:
    :return: Str - the name of the tagged image.
    - Looks like "dockerhub.com/james/repo:tagged"
    """
    tagged_name = repo + ":" + tagged
    cli.tag(image_id, repo, tagged)
    logging.info('Tagged ' + image_id + " " + tagged)
    return tagged_name


def run_container(image, container_name, args):
    """
    Run a container from an image.
    :param image: Str - the id or name of the image to run container from.
    :param container_name: Str - the name to give the container.
    :param args: Str or List - the command to run in the container.
    :return: Str - the id of the generated container.
    - Note - the output is ran through the threaded logging.info generator method.
    """
    container = cli.create_container(image=image, name=container_name, detach=True, command=args)  # Returns dict
    container_id = container['Id']  # Get id from dictionary
    cli.start(container_id)  # Start the container
    logging.info('Started container: ' + container_name + ' with commands: ' + "'{}'".format(args))
    print_threaded_generator(cli.logs(container=container_id, stdout=True, stream=True))  # Output logs in real time
    return container_id


def remove_container(container):
    """
    Kill and delete a container.
    :param container: Str - id or name of container to remove.
    :return: None
    """
    cli.stop(container=container)
    cli.remove_container(container=container, v=True) # v=True means force remove
    logging.info('Removed container: ' + container)


def inside_container(container_id, args):
    """
    Run command inside a running container. Similar to "docker exec ..."
    :param container_id: Str - the id of the container to run commands in
    :param args: Str or List - commands to run inside the container.
    :return: None
    """
    executor = cli.exec_create(container=container_id, cmd=args)
    exec_id = executor['Id']
    logging.info('Running inside container: ' + container_id + ' with commands: ' + "'{}'".format(args))
    cli.exec_start(exec_id=exec_id, stream=True, detach=True)


def login(**credentials):
    """
    Logs in to a docker registry, defaults to dockerhub at 'https://index.docker.io/v1/'
    :param login: Dict - {'username':None, 'password':None, 'email':None, 'registry':None, 'reauth':None, 'dockercfg_path':None}
    :return: None
    """
    login_data = cli.login(**credentials)
    status = login_data.get('Status')
    if status is not None:
        logging.info(status)
    else:
        logging.info('Failed to login. You may have logged in already, or the login credentials are invalid.')
