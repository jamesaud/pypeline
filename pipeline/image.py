from .container import Container
import config.docker_client as dc


class Image(object):
    def __init__(self, image_tag, build=False, path=None):
        if build:
            if not path:
                raise TypeError("You must specify a path!")
            # Call(['docker', 'build', '-t', image_tag, '.'])
            dc.build(path, image_tag) # Build in the current directory
        self.name = image_tag
        data = dc.find_image_by_name(self.name) # Lots of related information of the image
        if not data:
            raise TypeError("This image is invalid, docker tried to find the image with the given or generated name,",
                            image_tag, "but didn't find anything.")
        # data[0] is the dictionary contained in the list
        self.id = data[0]['Id'].split('sha256:')[-1]  # Get the unique ID number only


    #Run container with optional args
    #String -> Container
    def container(self, args=''):
        return Container(self.id, args) #Random unique container name.

    # Remove the image
    def remove(self):
        #call(['docker', 'rmi', '-f', self.id])
        dc.remove_image(self.id)

    # Pushes image, defaults to dockerhub
    def push(self):
        #call(['docker', 'push', self.name])
        dc.push(self.name)

    # Tags an image
    def tag(self, repo, tagged='latest'):
        self.name = dc.tag(self.id, repo, tagged)
        return self

    #Implement 'with' functionality
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.remove()
