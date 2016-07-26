import multiprocessing as mp
import logging
from pypeline.config.config import DEFAULT_REGISTRY
from pypeline.pipeline.pipeline import Pipeline


#Improve - the repository should have login credentials as a parameter option.
class GenericPipeline(object):
    """
    GenericPipeline is a pipeline to be implemented by other specific uses.
    Automation involves:
    - test commands automatically create containers.
    """

    def __init__(self):  # Takes a git url to a rails app
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
        self.pipe = Pipeline()
        self.dockerfile_dir = None
        self.repository = None
        self.registry = None
        self.git_url = None
        self.image = None

    # Tag the image correctly
    def _tag(self, tag):
        """
        Tag the image correctly. Should looke like registry/repo/image:tag
        :param tag: Str - the tag to give the image. This is the part of the url that is after ":"
        :return: None
        Notes - could look like 'registry.com/james/myrepo/myimage:latest'
        """
        def parse_repo_name(git_url):
            return git_url.split('/')[-1].lower()  # Get everything after 'github.com/' and lowercase it.
        if self.registry == DEFAULT_REGISTRY:
            base_docker_tag_url = ''
        else:
            base_docker_tag_url = self.registry
        self.image.tag(base_docker_tag_url + self.repository + '/' + parse_repo_name(self.git_url) + ':' + tag)  # Set the image tag.

    def test(self, *commands):
        """
        Run commands inside a container.
        :param commands: Str - commands to run in the container.
        - Note - Runs multiple threads to run concurrent containers and generate live output.
        :return: None
        """
        self.image.run_parallel_containers(*commands)  # list of commands being executed

    def _clone(self, git_url):
        """
        Clone git repository. If the user doesn't have a dockerfile, the default Dockerfile is automatically added to
        the directory!
        :return: None
        """
        self.pipe.clone(git_url)

    def build(self, git_url, dockerfile_dir='.', dockerfile_name='Dockerfile'):
        """
        Build image from the cloned repository using the self-provided dockerfile.
        :param dockerfile_path: Relative path to the dockerfile, including the name
        :return: None
        """
        self.git_url = git_url
        self._clone(git_url)
        self.dockerfile_dir = dockerfile_dir
        self.image = self.pipe.build(path=dockerfile_dir, dockerfile=dockerfile_name)

    def push(self, tag='latest'):
        """
        Push image to repository.
        :param tag: Str - the tag to give the image. Could be 'v2'. Defaults to 'latest'.
        :return: None
        """
        self._tag(tag)
        self.image.push()
        self.print_info()

    def print_info(self):
        print('Pushed image to repository ' + self.image.name)
        if self.registry == DEFAULT_REGISTRY:  # Print the dockerhub url if relevant.
            print('See it on your browser at dockerhub.com/r/' + self.image.name.split(':')[0])  # Get rid of the tag.

    def login(self, username=None, password=None, registry=DEFAULT_REGISTRY, repository=None):
        def _add_trailing_slash(url):
            return url + '/' if url[-1] != '/' else url  # If the ending slash is not in the URL given, then add it.

        def _remove_trailing_slash(url):
            return url if url[-1] != '/' else url[:-1]

        if repository is None:  # Set repository the same as the git account.
            repository = username

        self.repository = _remove_trailing_slash(repository)
        self.registry = _add_trailing_slash(registry)
        self.pipe.login(username=username, password=password, registry=registry)

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

