## Pypeline
A docker pipeline built in python. The ability to execute and design workflows. It might look like:

*clone from github - build docker image - run tests in docker container(s) - push to docker repository*

## Code Examples
The **pipeline** module and **generic pipeline** module allow you to generate pipelines.
Please checkout the examples in 'examples' for full code.

### Pipeline
Create complex pipelines that allow for fast and flexible docker deployments. 

It is build upon [docker-py](https://github.com/docker/docker-py/blob/master/docs/api.md "dockerpy"), a python wrapper around the REST api of the docker daemon.

This first example is drawn out and done 'the long way', but showcases some of the important operations available.

Before being able to do any pipeline code, you have to specify where the docker daemon is. You also might need to provide TLS configuration. If using 'default=True', the TLS config looks for the default.

`clientsetup(default=True, docker_base_url='https://192.168.99.100:2376')`

default=True 

Or on unix:

`clientsetup(docker_base_url=unix://var/run/docker.sock)`

Refer to [the docker-py api](https://github.com/docker/docker-py/tree/master/docs "the docker-py api").
```python
from pypeline.pipeline import Pipeline
from pypeline.config import clientsetup

clientsetup(default=True, docker_base_url='https://192.168.99.100:2376')
with Pipeline() as pipe:
    pipe.clone('https://github.cerner.com/JA048043/docker_test')  # clone from git
    test_image = pipe.build('justatest1232123/myawesomeimage')  # build with name
    container = test_image.container('echo "rspec"') # run commands in container
    container.run()  # creating and then running containers follows the docker daemon REST api
    container.remove()  # delete.
    test_image.tag('justatest1232123/myawesomeimage:solid')  # Tag it with a solid name
    pipe.login(username='justatest1232123', password='Justatest123')  # Login to dockerhub
    test_image.push()  # Push.
    test_image.remove()  #Remove the image, if you really want.
```

However, it is possible and recommended to make the code much more compact.
Python's 'with' syntax provides an automatic closure at the end of the block.
```python
with Pipeline() as pipe:
        pipe.clone('https://github.cerner.com/JA048043/docker_test')
        with pipe.build() as myImage, myImage.run_container('echo "unit-tests"'):
            myImage.tag("dockerhub.cerner.com/jamesaudretsch/myawesomeimage:latest").push()
#  The image and container are automatically deleted when the block ends.
```

### Generic Pipeline
The easiest but less flexible way to build a pipeline. The goal of the Generic Pipeline is to streamline the process for testing on a single image. It also hands all of the naming for you, so this example is pushed to the repository at 'dockerhub.com/r/justatest1232123/simplest_docker'. If you use a custom registry and repository name, it will be pushed to that location instead.

```python
from pypeline.generic_pipeline import GenericPipeline
from pypeline.config import clientsetup

clientsetup(default=True, docker_base_url='https://192.168.99.100:2376')
with GenericPipeline() as GP:
        GP.build('https://github.com/jamesaud/simplest_docker')  # Clone and build.
        GP.test('echo "first test"', 'echo "second test"', 'echo "third test"')  # Run parallel commands in separate containers
        GP.login(username='justatest1232123', password='Justatest123')  # Optional registry and repository argument
        GP.push('latest')  # Tag before it pushes.
```

Look in the examples folder for full examples of these two modules.

*generic-cline.py* is an example of a built generic pipeline that allows for command line input.

>python3 generic-cline.py --username justatest1232123 --password Justatest123 --url \

>https://github.cerner.com/JA048043/docker_test --test 'echo "hello world"' --test 'echo "hi"'


## Motivation

###Problem Statement
Manually doing CI/CD using docker can be a bloated process, including configuration and naming of images, maintaining and versioning containers and images, deleting old images and containers, etc. Moreover, the same process is consistently used over different images so we end up repeating ourselves.

###Goal
To provide a clear structure for building CI/CD pipelines with docker. This is an Object Oriented approach to building pipelines that requires very little code to get up and running.

## Installation
Make sure you have python3.

You must have git installed with command line input, because the pipeline uses the shell command 'git clone'.

How to install:

>git clone https://github.cerner.com/JA048043/pypeline

>cd pypeline

>pip3 install -r requirements.txt

>python3 setup.py install

##**API Reference**

##-Pipeline-

>from pypeline.pipeline import Pipeline

### clone

Clone from git repository. Just like the git clone command

**Params**:

* git_url (str): The url of the project to clone.

**Returns** None

### build

Builds from the cloned directory.

**Params**:

* image_tag (str): The name to give the image. : optional

* path (str): The relative path to the dockerfile : optional

* dockerfile (str): The name of the dockerfile  : optional

**Returns** Image: an image object representing this docker image.

### pull

Pulls an image, just like 'docker pull ...'

**Params**:

* image_tag (str): The url of the image to pull.

**Returns** Image: an image object representing the docker image.

### close

Closes the Pipeline. Because pipeline creates a directory to keep everything separated from the rest of your files, this function must be called at the end of the pipeline. Using 'with' syntax calls this command.

**Params**:

**Returns** (generator or str): The logs or output for the image

### copy_to_cloned_directory

Copys a single file into the cloned directory.

**Params**:

* full_file_path (str): The path to the file you wish to copy into the cloned directory.

**Returns** None

###login

Logs into dockerhub, or another registry, using a username and password.

**Params**:

* username (str): The username for the registry. : optional
 
* password (str): The password for the registry. : optional

* registry (str): The url of the registry to login to. : optional

**Returns** None

##-Image-

>from pypeline.pipeline import Image

Image is a representation of a docker image. It is returned when calling 'Pipeline().build' or 'Pipeline().pull'. You *could* also use it independently of pipeline...

###Properties:

* id : the id of the image. : read-only

* name: the name of the image. : read-only

###container

Creates a docker container based on the image. Does **not** run it.

Use either \<Container\>.run(), or \<Image\>.run_container() to run a container.

**Params**:

* args (str): The args to run inside the container : optional

* name (str): The name to give the docker container : optional

**Returns** Container : a container object representing a docker container.

###run_container

Same as 'container' but runs the container immediately. Is usually advised unless you have a reason to forgo running the container.

**Params**:

* args (str): The args to run inside the container : optional

* name (str): The name to give the docker container : optional

**Returns** Container : a container object representing a docker container.

###run_parallel_containers

Runs containers in parallel.  

**Params**:

* \*commands (str): Any amount of comma separated commands to run. Each separated command will be run in a separate container.

**Returns** None

###remove

Deletes the image. Is called when using 'with' syntax.

**Params**:

**Returns** None

###tag

Tags the image, and returns a new image

**Params**:

* name (str): The new name to give the image.

**Returns** Image (Self): returns itself with the tagged name.

###push

Pushes to registry. Like 'docker push ...'. Follows the same rules as regular docker. If you want to push to a private registry prepend the name of the image with 'registry.com/repo/image:tag'. To push to docker just keep the image name 'repo/image:tag'

**Params**:

**Returns** None

##-Container-

from pypeline.pipeline import Pipeline

Container is a representation of a docker container.

###Properties:

* id : the id of the container. : read-only

* name: the name of the container. : read-only

###remove

Removes the container.

**Params**:

**Returns** None

###run

Runs the container.

**Params**:

**Returns** None

##-GenericPipeline-

>from pypeline.generic_pipeline import GenericPipeline

###build

Builds a docker image from the git directory.

**Params**:

* git_url (str): The url of the github project.

* path (str): The relative path to the dockerfile : optional

* dockerfile (str): The name of the dockerfile  : optional

**Returns** None

###test

Runs commands inside of parallel containers.

**Params**:

* \*commands : commands to run in containers based on the built image. Any number of comma separated arguments.

**Returns** None

###login

Logs into a docker registry. Also provides the naming for the image this way. If using dockerhub, your image will look like: 'username/git_project_name:tag'

If logging into a private repository, you'll need to provide the repository argument to tell it where to upload.

>GenericPipeline().login(registry='privaterepo@dockerregistry.hub, repository='myname')

Your image will look like: 'registry/repo/git_project_name:tag'

**Params**:

* username (str) : the username for the repository : optional
* password (str) : the password for the repository : optional 
* registry (str) : the registry to upload to, defaults to dockerhub. 
* repository (str) : only required if providing the registry, tells the generic pipeline which repository to upload to if not provided a username : optional

**Returns** None

###push

Pushes the image.

**Params**:

**Returns** None

###close

Closes the Pipeline() that was opened. Is called automatically using 'with' syntax.

**Params**:

**Returns** None

## Tests

Unit tests are only provided for the pipeline, not the generic pipeline. They are in the unit_tests folder. Something to note is that a side effect of testing might be that a small busybox or alpine image remains on your machine.

## Contributors

James Audretsch: jamaudre@indiana.edu james.audretsch@cerner.com

## License
