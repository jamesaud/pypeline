import docker
import logging

"""
The functions in this file are wrappers over the dockerpy api, an api for communicating directly with the docker client.
References - Refer to  'https://github.com/docker/docker-py/blob/master/docs/api.md'  for the docker-py api
"""

class DockerClient:
    cli = None

    @classmethod
    def assign_client(cls, client):
        if cls.cli is None:
            cls.cli = client

    @classmethod
    def print_generator(cls, generator, info=None):
        """
        Prints line by line from a generator, but makes it threaded.
        :param generator: Generator Stream- The generator to print.
        :param info: Str - name to prepend generator output. Generally an id or name.
        :return: None
        """
        message = b''
        if info:
            message += str.encode(info) + b": "
        for line in generator:
            logging.info(message + line)


    # Improve - should have option for registry and login credentials.
    @classmethod
    def pull(cls, image_name):
        """
        Pull image from registry, defaults to dockerhub.com.
        :param image_name: Str - the name of the image to pull.
        :return: None
        """
        generator = cls.cli.pull(image_name, stream=True)
        cls.print_generator(generator)


    # Find by image id
    @classmethod
    def find_image(cls, image_id):
        """
        Find image by id.
        :param image_id: Str - the id of the image to find.
        :return: Dict - a dictionary containing details about the image.
        """
        return cls.cli.inspect_image(image_id)

    @classmethod
    def find_image_by_name(cls, image_name):
        """
        Find image by name.
        :param image_name: Str - the name of the image to search for.
        :return: List - a list containing a dictionary containing details about the image...IDK why the api works like that.
        """
        return cls.cli.images(image_name)

    @classmethod
    def find_container(cls, container_id):
        """
        Find the container by id.
        :param container_id: Str - the id of the container to search for.
        :return: Dict - a dictionary containing details about the container.
        """
        return cls.cli.inspect_container(container_id)

    @classmethod
    def remove_image(cls, image):
        """
        Remove the image.
        :param image: Str - the id or name of the image.
        :return: None
        """
        cls.cli.remove_image(image, True)
        logging.info("Removed image: " + image)

    @classmethod
    def remove_container(cls, container):
        """
        Kill and delete the container
        :param container: Str - id or name of the container.
        :return: None
        """
        cls.cli.remove_container(container, True)
        logging.info("Removed container : " + container)

    @classmethod
    def build(cls, dockerfile_path, image_name, dockerfile=None):
        """
        Build image from dockerfile in specified path.
        :param dockerfile_path: Str - full path of the dockerfile.
        :param image_name: Str - name to give the image.
        :return: None
        """
        logging.info("Building image " + image_name)
        logs_generator = cls.cli.build(path=dockerfile_path, rm=True, tag=image_name, dockerfile=dockerfile)
        cls.print_generator(logs_generator)


    # Improve - should be able to give repository login credentials.
    @classmethod
    def push(cls, image_name):
        """
        Push image to repository.
        :param push_name: the name of the image to push.
        :return: None
        """
        cls.print_generator(cls.cli.push(image_name, stream=True))


    # Improve - use the docker api to get the actual tag of the image, not creating it with by hand. Might run into errors
    #           where it is not the same as the actual name.
    @classmethod
    def tag(cls, image_name, repo, tagged):
        """
        Re-Tag an image. Same as 'docker tag image tagName'
        :param image_id:
        :param repo:
        :param tag:
        :return: Str - the name of the tagged image.
        - Looks like "myimage:tagged"
        """
        tagged_name = repo + ":" + tagged
        cls.cli.tag(image_name, repo, tagged)
        logging.info('Tagged ' + tagged_name)
        return tagged_name

    @classmethod
    def create_container(cls, image, container_name, args):
        """
        Creates a container but does not run it.
        :param image: Str - name or id of image to build
        :param container_name: Str - name to give container
        :param args: Str - commands to give container
        :return: Str - id of the container
        """
        container = cls.cli.create_container(image=image, name=container_name, detach=True, command=args)  # Returns dict
        logging.info('Created container (did not run yet) with commands: ' + args)
        return container['Id']  # Get id from dictionary

    @classmethod
    def run_container(cls, container_id):
        """
        Run a container from an image.
        :param image: Str - the id or name of the image to run container from.
        :param container_name: Str - the name to give the container.
        :param args: Str or List - the command to run in the container.
        :return: Dict - the id of the generated container.
        - Note - the output is ran through the threaded logging.info generator method.
        """
        cls.cli.start(container_id)  # Start the container
        logging.info('Running container: ' + container_id)
        logs = cls.cli.logs(container=container_id, stdout=True, stream=True)
        cls.print_generator(logs, container_id)

    @classmethod
    def remove_container(cls, container):
        """
        Kill and delete a container.
        :param container: Str - id or name of container to remove.
        :return: None
        """
        cls.cli.stop(container=container)
        cls.cli.remove_container(container=container, v=True)  # v=True means force remove
        logging.info('Removed container: ' + container)


    # def inside_container(container_id, args):
    #     """
    #     Run command inside a running container. Similar to "docker exec ..."
    #     :param container_id: Str - the id of the container to run commands in
    #     :param args: Str or List - commands to run inside the container.
    #     :return: Generator
    #     """
    #     executor = cls.cli.exec_create(container=container_id, cmd=args)
    #     exec_id = executor['Id']
    #     logging.info('Running inside container: ' + container_id + ' with commands: ' + "'{}'".format(args))
    #     cls.cli.exec_start(exec_id=exec_id, stream=True, detach=True)

    @classmethod
    def login(cls, username=None, password=None, registry=None):
        """
        Logs in to a docker registry, defaults to dockerhub at 'https://index.docker.io/v1/'
        :param login: Dict - {'username':None, 'password':None, 'email':None, 'registry':None, 'reauth':None, 'dockercfg_path':None}
        :return: None
        """
        login_data = cls.cli.login(username=username, password=password, registry=registry)
        status = login_data.get('Status')
        if status is not None:
            logging.info(status)
        else:
            logging.info('Failed to login. You may have logged in already, or the login credentials are invalid.')


