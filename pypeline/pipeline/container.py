from uuid import uuid4

import pypeline.config.docker_client as dc


class Container(object):
    """
    A Container represents a docker container. It carries relevant information in order to access the container with
    the docker api and methods for interacting with a docker container.
    """
    # Improve - self.__nametag__ and self.__id__ should be private properties.
    def __init__(self, image_name, args=''):
        """Initializes the container object with the corresponding docker container details.
        :param image_id: Str - the id of the image to build the container from.
        :param args: Str - the command to run in the docker container.
        :attribute name: Str - the name of the docker container.
        :attribute id: Str - the id of the docker container.
        """
        if not args:  # Run an arbitrary command so docker doesn't error in some cases.
            args = 'false'
        self.__nametag__ = str(uuid4())
        self.__id__ = dc.create_container(image_name, self.__nametag__, args) # Equivalent to 'docker run --name name args'
        dc.run_container(self.__id__)


    def remove(self):
        """Kill and delete the container.
        :return: None
        """
        dc.remove_container(self.__id__)

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
