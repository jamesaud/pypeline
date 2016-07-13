from .container import Container
import config.docker_client as dc


# Improve - Make name and id private properties.
class Image(object):
    """
    An Image represents a docker image. It carries relevant information in order to access the image with the docker api
    and methods for interacting with a docker image.
    """
    def __init__(self, image_tag, build=False, path=None):
        """Initialize the image and build the docker image if specified. Image captures a docker image's essential data.
        :param image_tag: Str - the name to give the image.
        :param build: Bool - True to build from the specified dockerfile path.
        :param path: Str - the path to the dockerfile relative to the cloned directory.
        :attribute self.name: Str - the name of the docker image.
        :attribute self.id: Str - the id of the docker image.
        """
        if build:
            if not path:  # If build is True, there must be a specified path
                raise TypeError("You must specify a path!")
            dc.build(path, image_tag)  # Build docker image from the specified directory
        self.name = image_tag
        data = dc.find_image_by_name(self.name)  # Dictionary with related information of the image
        if not data:
            raise TypeError("The image is invalid, docker tried to find the image with the given or generated name,",
                            image_tag, "but didn't find anything.")
        self.id = data[0]['Id'].split('sha256:')[-1]  # Get the unique ID number only

    def container(self, args=''):
        """Create and run a container with given commands.
        :param args: String - the commands to run in a docker container.
        :return: Container
        """
        return Container(self.id, args) #Random unique container name.

    def remove(self):
        """Delete the image.
        :return: None
        """
        dc.remove_image(self.id)

    # Improve - option to push to specified registry.
    def push(self):
        """Push image (the registry should be in the name) to registry.
        :return: None
        """
        dc.push(self.name)

    def tag(self, repo, tagged='latest'):
        """Tag the image. Similar to 'docker tag ...'.
        :param repo: Str - the registry + repo name eg. 'dockerhub.com/james/myrepo'
        :param tagged: Str - the tag to give the image. eg. 'coolv2'. Defaults to 'latest'
        :return: self
        - The image name will now be repo:tag, eg. self.name = 'dockerhub.com/james/myrepo:coolv2'
        """
        self.name = dc.tag(self.id, repo, tagged)
        return self

    def __enter__(self):  # Implement 'with' functionality
        return self

    def __exit__(self, exc_type, exc_value, traceback):  # Implement 'with' functionality
        self.remove()
