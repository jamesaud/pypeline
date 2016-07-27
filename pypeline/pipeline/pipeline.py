import os
import shutil
from shutil import copy
from subprocess import call
from uuid import uuid4
from pypeline.config.docker_client import DockerClient
from .image import Image


class Pipeline(object):
    """
    A pipeline is a workspace with methods to do the pipeline process.
    The pipeline process is: clone from Git, build image, run containers, push image to repository.
    """
    def __init__(self):
        """
        Initialize class, create work directory and chdir into it.
        :attribute self.work_directory: Str - The full path of the work directory.
        :attribute self.cloned_directory: Str -The full path of the github cloned directory.
        """
        work_directory = str(uuid4())
        os.makedirs(work_directory)  # Creates workspace for this pipeline
        self.cloned_directory = None  # Set when calling self.clone()
        print(os.getcwd())
        print(work_directory)
        self.work_directory = os.path.abspath(os.path.join(os.getcwd(), work_directory))  # Save as full path

    def clone(self, git_url):
        """
        Clones code from Github.
        :param git_url: Str - the url to clone from
        :return: None
        """
        git_workspace = str(uuid4())
        self.cloned_directory = os.path.join(self.work_directory, git_workspace)  # Path looks like 'work_directory/git_directory'
        call(['git', 'clone', git_url, self.cloned_directory])  # Clone in a unique directory.

    def build(self, image_tag=str(uuid4()), path='.', dockerfile='Dockerfile'):
        """
        Build image in cloned directory, or user specified path relative to the cloned directory.
        :param image_tag: Str - the docker name to give the image. Creates a name if not given.
        :param directory: Str - the directory path relative to the cloned directory. Defaults to '.', the top level.
        :return: Image
        """
        path_to_dockerfile = os.path.join(self.cloned_directory, path)  # Full path to the dockerfile
        return Image(image_tag, build=True, path=path_to_dockerfile, dockerfile=dockerfile)  # Build = True.


    def pull(self, image_tag):
        """
        Pull docker image from dockerhub.
        :param image_tag: Str - the docker image to pull.
        :return: Image
        """
        DockerClient.pull(image_tag)  # Pulls the docker image to the machine.
        return Image(image_tag)

    def close(self):
        """
        Delete the work directory.
        :return: None
        """
        try:
            os.chdir(self.work_directory)
            os.chdir('..')
            shutil.rmtree(self.work_directory, ignore_errors=True) #Remove the workspace recursively.
        except OSError as e:
            print(e, "The pipeline tried and failed to delete directory at ", self.work_directory)

    def copy_to_cloned_directory(self, full_file_path):
        """
        Copy a file into the cloned directory.
        :param full_file_path: Str - the full path of the file to copy.
        :return: None
        """
        try:
            copy(full_file_path, self.cloned_directory)
        except TypeError as e:
            print(e, " Are you sure you cloned from git?")

    @staticmethod
    def login(username=None, password=None, registry=None):
        """
        Logs in to a docker registry, defaults to dockerhub at 'https://index.docker.io/v1/'
        :param username: Str - the username to the account.
        :param password: Str - the password to the account.
        :param registry: Str - the registry to upload to. Not required if using dockerhub.
        :return: None
        """
        DockerClient.login(username=username, password=password, registry=registry)

    def __enter__(self):  # Implement 'with' functionality
        return self

    def __exit__(self, exc_type, exc_value, traceback):  # Implement 'with' functionality
        self.close()
