import os
import re
from pipeline.pipeline import Pipeline
from config import config

class RailsPipeline(object):
    dockerfile = os.path.abspath(config.RAILS_DOCKERFILE_LOCATION)# Location of dockerfile

    def __init__(self, git_url, registry_url, dockerfile_dir='.'): # Takes a git url to a rails app
        self.git_url = git_url
        self.dockerfile_dir = dockerfile_dir
        self.registry_url = registry_url
        self.image = None
        self.pipe = Pipeline()

    # Runs shell test commands in container(s?) of given image
    def test(self, *commands):
        for command in commands: # Or should we run all tests in the same container?
            with self.image.container(command):  # Run each command in parallel in its own container
                pass

    # tags the image correctly
    def _tag(self, tag):
        def parse_repo_name():
            return self.git_url.split('.com/')[-1].lower() # Get everything after github.com/ and lowercase it

        self.image.tag(self.registry_url + '/' + parse_repo_name(), tag)

    def clone(self):
        self.pipe.clone(self.git_url)
        self.pipe.copyToClonedDirectory(self.dockerfile)  # Copy dockerfile to the cloned directory

    # Return build image
    def build(self):
        self.image = self.pipe.build(directory=self.dockerfile_dir)

    def push(self, tag='latest'):
        self._tag(tag)
        self.image.push()
        self._printUploadURL()

    def _printUploadURL(self):
        def fix_url(): # Returns string of image_tag with /v2/
            remove_tag = self.image.name.split(':')[0]
            insert_v2 = re.sub('.com/', '.com/v2/', remove_tag)
            return insert_v2
        final_url = fix_url() + '/tags/list'
        print("\nYou can verify your pushed docker image at: " + final_url)
        print("or run the following command from terminal: docker pull " + self.image.name)

    def close(self):
        self.pipe.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
