from pypeline.config.docker_client import DockerClient as dc
from .container import Container


# Improve - Make name and id private properties.
class Image(object):
    """
    An Image represents a docker image. It carries relevant information in order to access the image with the docker api
    and methods for interacting with a docker image.
    """
    def __init__(self, image_tag, build=False, path=None, dockerfile=None):
        """Initialize the image and build the docker image if specified. Image captures a docker image's essential data.
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
        self.__id__ = data[0]['Id'].split('sha256:')[-1]  # Get the unique ID number only

    def container(self, args='', run_now=True):
        """Create and run a container with given commands.
        :param args: String - the commands to run in a docker container.
        :return: Container
        """
        container = Container(self.__id__, args)  # Random unique container name.
        if run_now:
            container.run()
        return container

    """
    NEW CODE FOR MULTI CONTAINER PARLELL RUNNING
    Change the above container function to just return a container without running it.
    Write a run_container function to do what container function currently does.
    Call parallel_containe like image.run_parallel_containers(image.container('rpec spec'), image.container('rspec spec'))
    figure out how to multithread it.
    """

    def run_parallel_containers(self, *args):
        # for container in args:
            # Multithread:
            # container.run()
        pass

    def remove(self):
        """Delete the image.
        :return: None
        """
        dc.remove_image(self.__nametag__)

    # Improve - option to push to specified registry.
    def push(self):
        """Push image (the registry should be in the name) to registry.
        :return: None
        """
        dc.push(self.__nametag__)

    def tag(self, repo, tagged='latest'):
        """Tag the image. Similar to 'docker tag ...'.
        :param repo: Str - the registry + repo name eg. 'dockerhub.com/james/myrepo'
        :param tagged: Str - the tag to give the image. eg. 'coolv2'. Defaults to 'latest'
        :return: self
        - The image name will now be repo:tag, eg. self.__nametag__ = 'dockerhub.com/james/myrepo:coolv2'
        """
        self.__nametag__ = dc.tag(self.__nametag__, repo, tagged)
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
