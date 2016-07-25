from uuid import uuid4

from pypeline.config.docker_client import DockerClient as dc


class Container(object):
    """
    A Container represents a docker container. It carries relevant information in order to access the container with
    the docker api and methods for interacting with a docker container.
    """
    # Improve - self.__nametag__ and self.__id__ should be private properties.
    def __init__(self, image_name, args='', container_name=None):
        """Initializes the container object with the corresponding docker container details.
        :param image_name: Str - the name of the image to build the container from.
        :param args: Str - the command to run in the docker container.
        :attribute name: Str - the name of the docker container.
        :attribute id: Str - the id of the docker container.
        """
        if not args:  # Run an arbitrary command so docker doesn't error in some cases.
            args = 'false'
        self.__nametag__ = container_name or str(uuid4())
        self.__id__ = self._create(image_name, self.__nametag__, args)


    def remove(self):
        """
        Kill and delete the container.
        :return: None
        """
        dc.remove_container(self.__id__)

    def _create(self, image_name, name, args):
        return dc.create_container(image_name, name, args)

    def run(self):
        dc.run_container(self.__id__)

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
