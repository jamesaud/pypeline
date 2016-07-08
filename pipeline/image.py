from subprocess import call, Popen, PIPE
from uuid import uuid4
from container import Container

class Image(object):
    def __init__(self, image_tag, build=False):
        if build:
            call(['docker', 'build', '-t', image_tag, '.'])
        self.name = image_tag
        self.id = None
        with Popen('docker inspect --format="{{.Id}}" ' + image_tag, shell=True, stdout=PIPE).stdout as stdout:
            self.id = stdout.read().strip() #ID is the SHA256 Unique ID docker gives the image

    #Run container with optional args
    #String -> Container
    def container(self, args=''):
        uniqueName = str(uuid4())
        return Container(self.id, uniqueName, args) #Random unique container name.

    #Remove the image
    def remove(self):
        call(['docker', 'rmi', '-f', self.id])

    #Pushes image, defaults to dockerhub
    def push(self):
        call(['docker', 'push', self.name])

    #Tags an image
    def tag(self, tag):
        self.name = tag
        call(['docker', 'tag', self.id, tag])
        return self

    #Implement 'with' functionality
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.remove()
