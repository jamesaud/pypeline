from .threaded import Parallel
from pypeline.config.docker_client import DockerClient as dc
from .container import Container


# Improve - Make name and id private properties.
class Image(object):
    """
    An Image represents a docker image. It carries relevant information in order to access the image with the docker api
    and methods for interacting with a docker image.
    """
    def __init__(self, image_tag, build=False, path=None, dockerfile=None):
        """
        Initialize the image and build the docker image if specified. Image captures a docker image's essential data.
        :param image_tag: Str - the name to give the image.
        :param build: Bool - True to build from the specified dockerfile path.
        :param path: Str - the path to the dockerfile relative to the cloned directory.
        :attribute self.name: Str - the name of the docker image.
        :attribute self.__id__: Str - the id of the docker image.
        """
        if build:
            if not path:  # If build is True, there must be a specified path
                raise TypeError("You must specify a path!")
            dc.build(path, image_tag, dockerfile=dockerfile)  # Build docker image from the specified directory
        self.__nametag__ = image_tag
        data = dc.find_image_by_name(self.__nametag__)  # Dictionary with related information of the image
        if not data:
            raise TypeError("The image is invalid, docker tried to find the image with the given or generated name,",
                            image_tag, "but didn't find anything.")
        self.__id__ = data[0]['Id'].split('sha256:')[-1]  # Get the unique ID number only by parsing the daemon output.

    def container(self, args='', name=None):
        """
        Create  a container with given commands.
        :param args: String - the commands to run in a docker container.
        :return: Container - a new container.
        """
        container = Container(self.__id__, args, name)  # Random unique container name.
        return container

    def run_container(self, args='', name=None):
        """
        Create and run a container with given commands.
        :param args: String - the commands to run in a docker container.
        :param name: String - the name to give the container.
        :return: Container - a running container
        """
        container = Container(self.__id__, args, name)  # Random unique container name.
        container.run()
        return container

    def run_parallel_containers(self, *commands):
        """
        Run commands in parallel, multi-threaded containers.
        :param commands: Str - each separated string is run in a new container.
        :return: None
        """
        parallel = Parallel()
        for command in commands:
            parallel.add(self.container(command).run)
        parallel.run()

    def remove(self):
        """
        Delete the image.
        :return: None
        """
        dc.remove_image(self.__nametag__)

    # Improve - option to push to specified registry.
    def push(self):
        """
        Push image (the registry should be in the name) to registry.
        :return: None
        """
        dc.push(self.__nametag__)

    def tag(self, name):
        """
        Tag the image.
        :param name: Str - the registry + repo name eg. 'dockerhub.com/james/myrepo'
\        :return: self
        - The image name will now be repo:tag, eg. self.__nametag__ = 'james/myrepo:coolv2'
        """
        try:
            split = name.split(':')
            name, tagged = split[0], split[1]
        except IndexError:
            repo, tagged = name, 'latest'
        self.__nametag__ = dc.tag(self.name, name, tagged)
        return self

    @property
    def id(self):
        return self.__id__

    @property
    def name(self):
        return self.__nametag__

    def __enter__(self):  # Implement 'with' functionality
        return self

    def __exit__(self, exc_type, exc_value, traceback):  # Implement 'with' functionality
        self.remove()
