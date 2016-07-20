import os
import shutil
from shutil import copy
from subprocess import call
from uuid import uuid4

from pypeline.config.docker_client import pull as dc_pull, login as dc_login
from .image import Image


class Pipeline(object):
    """
    A pipeline is a workspace with methods to do the pipeline process.
    The pipeline process is: clone from Git, build image, run containers, push image to repository.
    """
    def __init__(self):
        """Initialize class, create work directory and chdir into it.
        :attribute self.work_directory: Str - The full path of the work directory.
        :attribute self.cloned_directory: Str -The full path of the github cloned directory.
        """
        work_directory = str(uuid4())
        os.makedirs(work_directory)  # Creates workspace for this pipeline
        os.chdir(work_directory)
        self.cloned_directory = None  # Set when calling self.clone()
        self.work_directory = os.path.abspath('.')  # Save as full path

    def clone(self, git_url):
        """Clones code from Github.
        :param git_url: Str - the url to clone from
        :return: None
        """
        git_workspace = str(uuid4())
        call(['git', 'clone', git_url, git_workspace])  # Clone in a unique directory.
        self.cloned_directory = os.path.join(self.work_directory, git_workspace)  # Path looks like 'work_directory/git_directory'

    def build(self, image_tag=str(uuid4()), **directory):
        """Build image in cloned directory, or user specified path relative to the cloned directory.
        :param image_tag: Str - the docker name to give the image. Creates a name if not given.
        :param directory: Str - the directory path relative to the cloned directory. Defaults to '.', the top level.
        :return: Image
        """
        dockerDir = directory.get('directory')  # dict.get(value) can return None, dict[value] will raise an error.
        if not dockerDir:  # Check if optional directory argument was passed.
            dockerDir = '.'  # Default path the docker file is at.
        path_to_dockerfile = os.path.join(self.cloned_directory, dockerDir)  # Full path to the dockerfile
        return Image(image_tag, True, path_to_dockerfile)  # Build = True.

    @classmethod
    def pull(self, image_tag):
        """Pull docker image from dockerhub.
        :param image_tag: Str - the docker image to pull.
        :return: Image
        """
        dc_pull(image_tag)  # Pulls the docker image to the machine.
        return Image(image_tag)

    def close(self):
        """Delete the work directory.
        :return: None
        """
        try:
            os.chdir(self.work_directory)
            os.chdir('..')
            shutil.rmtree(self.work_directory, ignore_errors=True) #Remove the workspace recursively.
        except OSError as e:
            print(e, "The pipeline tried and failed to delete directory at ", self.work_directory)

    def copyToClonedDirectory(self, full_file_path):
        """
        Copy a file into the cloned directory.
        :param full_file_path: Str - the full path of the file to copy.
        :return: None
        """
        try:
            copy(full_file_path, self.cloned_directory)
        except TypeError as e:
            print(e, " Are you sure you cloned from git?")

    @classmethod
    def login(self, username=None, password=None, registry=None):
        """
        Logs in to a docker registry, defaults to dockerhub at 'https://index.docker.io/v1/'
        :param login: Dict - {'username':None, 'password':None, 'email':None, 'registry':None, 'reauth':None, 'dockercfg_path':None}
        :return: None
        """
        dc_login(username=username, password=password, registry=registry)

    def __enter__(self):  # Implement 'with' functionality
        return self

    def __exit__(self, exc_type, exc_value, traceback):  # Implement 'with' functionality
        self.close()
