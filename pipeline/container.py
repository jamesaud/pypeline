from subprocess import call, Popen, PIPE
import config.docker_client as dc
from uuid import uuid4

class Container(object):
    def __init__(self, image_id, container_name, args=''):
        if not args: #Run an arbitrary command so docker doesn't error in some edge cases where the user hasn't specified any commands.
            args = 'false'
        call(['docker', 'run', '-d', '--name',  container_name, image_id] + args.split())
        self.name = container_name #Will be a random string created in image.py
        self.id = None
        with Popen('docker inspect --format="{{.Id}}" ' + container_name, shell=True, stdout=PIPE).stdout as stdout:
            self.id = str(stdout.read().strip())[2:-1]

    #Run commands inside a running container.
    #This will error if the container isn't running.
    def inside(self, args='false'):
        call(['docker', 'exec', self.id] + args.split())

    #Remove the container
    def remove(self):
        call(['docker', 'rm', '-f', self.id])

    #Implement 'with' functionality
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.remove()
