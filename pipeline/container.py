from uuid import uuid4
import config.docker_client as dc

class Container(object):
    def __init__(self, image_id, args=''):
        if not args: #Run an arbitrary command so docker doesn't error in some cases.
            args = 'false'
        self.name = str(uuid4()) #Will be a random string created in image.py
        self.id = dc.run_container(image_id, self.name, args)

    #Run commands inside a running container.
    #This will error if the container isn't running.
    def inside(self, args='false'):
        dc.inside_container(self.id, args)

    #Remove the container
    def remove(self):
        dc.remove_container(self.id)

    #Implement 'with' functionality
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.remove()
