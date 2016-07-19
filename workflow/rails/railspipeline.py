import os
import re
import threading
from pipeline.pipeline import Pipeline
from config import config
from pipeline.image import Image


#Improve - the repository should have login credentials as a parameter option.
class RailsPipeline(object):
    """
    RailsPipeline is a pipeline focused on specific rails applications.
    Automation involves:
    - the dockerfile in 'config.RAILS_DOCKERFILE_LOCATION' is copied into the directory automatically.
    - test commands automatically create containers.
    """

    dockerfile = os.path.abspath(config.RAILS_DOCKERFILE_LOCATION)  # Location of dockerfile

    def __init__(self, git_url, registry_url, dockerfile_dir=None):  # Takes a git url to a rails app
        """
        Initializes the RailsPipeline object.
        :param git_url: Str - the git repo to clone from.
        :param registry_url: Str - the repository to push to
        :param dockerfile_dir: Str - the directory where the dockerfile is located relative to the github directory.
        :attribute self.git_url: Str - the given git url.
        :attribute self.dockerfile_dir: Str - the given dockerfile directory given.
        :attribute self.registry_url: Str - the given dockerfile directory.
        :attribute self.image: Image - the image build from the cloned repository. Is set in self.build()
        :attribute self.pipeline: Pipeline - the pipeline opened for the current object.
        """
        self.git_url = git_url
        self.dockerfile_dir = dockerfile_dir
        self.registry_url = registry_url
        self.image = None
        self.pipe = Pipeline()


    # Improve - run threaded containers in parallel
    def test(self, *commands):
        """
        Run commands inside a container.
        :param commands: Str - commands to run in the container.
        :return: None
        """
        containers = []  # List of all created containers
        for command in commands:  # Or should we run all tests in the same container?
            self.image.container(command)

    # tags the image correctly
    def _tag(self, tag):
        """
        Tag the image correctly. Should looke like registry/repo/image:tag
        :param tag: Str - the tag to give the image. This is the part of the url that is after ":"
        :return: None
        Notes - could look like 'dockerhub.com/james/myrepo/myimage:latest'
        """
        def parse_repo_name():
            return self.git_url.split('.com/')[-1].lower()  # Get everything after 'github.com/' and lowercase it.

        self.image.tag(self.registry_url + '/' + parse_repo_name(), tag)  # Set the image tag.

    def clone(self):
        """
        Clone git repository. If the user doesn't have a dockerfile, the default Dockerfile is automatically added to
        the directory!
        :return: None
        """
        self.pipe.clone(self.git_url)
        if not self.dockerfile_dir:  # If the user didn't provide their own dockerfile directory location.
            self.dockerfile_dir = '.'
            self.pipe.copyToClonedDirectory(self.dockerfile)

        elif 'Dockerfile' not in os.listdir(self.dockerfile_dir):  # If dockerfile isn't in the user given directory.
            raise OSError('There is not a dockerfile in the given directory: ', self.dockerfile_dir)

    def build(self):
        """
        Build image from the cloned repository using the self-provided dockerfile.
        :return: None
        """
        self.image = self.pipe.build(directory=self.dockerfile_dir)

    def push(self, tag='latest'):
        """
        Push image to repository.
        :param tag: Str - the tag to give the image. Could be 'v2'. Defaults to 'latest'.
        :return: None
        """
        self._tag(tag)
        self.image.push()
        self._printUploadURL()

    def _printUploadURL(self):
        """
        Print information about where the docker image was uploaded to.
        :return: None
        """
        def fix_url():  # Returns string of image_tag with /v2/
            remove_tag = self.image.name.split(':')[0]  # Get everything before the tag
            insert_v2 = re.sub('.com/', '.com/v2/', remove_tag)  # Replace /v2 in the url
            return insert_v2
        final_url = fix_url() + '/tags/list'  # Append tags/list
        print("\nYou can verify your pushed docker image at: " + final_url)
        print("or run the following command from terminal: docker pull " + self.image.name)

    def close(self):
        """
        Closes the pipeline to delete the work directory.
        :return: None
        """
        self.pipe.close()

    def __enter__(self):  # Implements 'with' functionality.
        return self

    def __exit__(self, exc_type, exc_value, traceback):  # Implements 'with' functionality.
        self.close()
