import os
import shutil

from subprocess import call
from uuid import uuid4
from shutil import copy
from pipeline.image import Image
from config.docker_client import pull as dc_pull

class Pipeline(object):
    def __init__(self):
        work_directory = str(uuid4())  # Creates workspace for this pipeline
        os.makedirs(work_directory)
        os.chdir(work_directory)
        self.cloned_directory = None
        self.work_directory = os.path.abspath('.')  # Save as full path

    # Clone from git url, and provide workspace
    def clone(self, git_url):
        git_workspace = str(uuid4())
        call(['git', 'clone', git_url, git_workspace])
        self.cloned_directory = os.path.join(self.work_directory, git_workspace)

    # Class Decorator: executes function in Clone directory, and returns to work directory.
    def _returnToWorkDir(function):
        def wrapper(self, *args, **kwargs):
            result = function(self, *args, **kwargs)
            os.chdir(self.work_directory)
            return result
        return wrapper

    # Build image in cloned directory, or specified directory
    def build(self, image_tag=str(uuid4()), **directory):
        dockerDir = directory.get('directory')
        if not dockerDir: # see if the user entered the optional argument
            dockerDir = '.' #Default path the docker file is at.
        path_to_dockerfile = os.path.join(self.cloned_directory, dockerDir)
        image = Image(image_tag, True, path_to_dockerfile)  # Build = True.
        return image

    # Pull Docker image
    # str -> Image
    def pull(self, image_tag):
        #call(['docker', 'pull', image_tag])
        dc_pull(image_tag)
        return Image(image_tag)

    def close(self):
        try:
            os.chdir(self.work_directory)
            os.chdir('..')
            shutil.rmtree(self.work_directory, ignore_errors=True) #Remove the workspace recursively.
        except OSError as e:
            print(e, "The pipeline tried to delete directory at ", self.work_directory)

    # Copys a file into the given path in the Cloned.
    def copyToClonedDirectory(self, full_file_path):
        try:
            copy(full_file_path, self.cloned_directory)
        except TypeError as e:
            print(e, " Are you sure you cloned from git?")

    # Implement 'with' functionality
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
