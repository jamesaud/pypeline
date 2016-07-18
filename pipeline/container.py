from uuid import uuid4
import config.docker_client as dc

class Container(object):
    """
    A Container represents a docker container. It carries relevant information in order to access the container with
    the docker api and methods for interacting with a docker container.
    """
    # Improve - self.name and self.id should be private properties.
    def __init__(self, image_name, args=''):
        """Initializes the container object with the corresponding docker container details.
        :param image_id: Str - the id of the image to build the container from.
        :param args: Str - the command to run in the docker container.
        :attribute name: Str - the name of the docker container.
        :attribute id: Str - the id of the docker container.
        """
        if not args:  # Run an arbitrary command so docker doesn't error in some cases.
            args = 'false'
        self.str = str(uuid4())
        self.id = dc.run_container(image_name, self.str, args)  # Equivalent to 'docker run --name name args'


    def inside(self, args):
        """Execute commands inside a running container. Error if container isn't running.
        :param args: Str - the command to run.
        """
        dc.inside_container(self.id, args)

    def remove(self):
        """Kill and delete the container.
        :return: None
        """
        dc.remove_container(self.id)

    def __enter__(self):  # Implement 'with' functionality
        return self

    def __exit__(self, exc_type, exc_value, traceback):  # Implement 'with' functionality
        self.remove()
