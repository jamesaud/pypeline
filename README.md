## Pypeline
A docker pipeline built in python. The ability to execute the following workflow:

*clone from github - build docker image - run tests in docker container(s) - push to docker repository*

## Code Examples
The **pipeline** module and **generic pipeline** module allow you to generate pipelines.
Please checkout the examples in 'examples' for full code.

### Pipeline
Create complex pipelines that allow for fast and flexible docker deployments. It is based on the [docker-py](https://github.com/docker/docker-py/blob/master/docs/api.md "dockerpy") api.

This first example is drawn out and done 'the long way', but showcases some of the important operations available.

Before being able to do any pipeline code, you have to specify where the docker daemon is. You also might need to provide TLS configuration. If using 'default=True', the TLS config looks for the default.

>clientsetup(default=True, docker_base_url='https://192.168.99.100:2376')

Or on unix:
>clientsetup(docker_base_url=unix://var/run/docker.sock)

Refer to https://github.com/docker/docker-py/blob/master/docs/api.md, the docker-py api.
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
## Motivation

###Problem Statement
Manually doing CI/CD using docker can be a bloated process, including configuration and naming of images, maintaining and versioning containers and images, deleting old images and containers, etc. Moreover, the same process is consistently used over different images so we end up repeating ourselves.

###Goal
To provide a clear structure for building CI/CD pipelines with docker. This is an Object Oriented approach to building pipelines that requires very little code to get up and running.

## Installation
Make sure you have python3
>git clone https://github.cerner.com/JA048043/pypeline


>cd pypeline


>python3 setup.py install

##API Reference

### Pipeline
#### attach

The `.logs()` function is a wrapper around this method, which you can use
instead if you want to fetch/stream container output without first retrieving
the entire backlog.

**Params**:

* container (str): The container to attach to
* stdout (bool): Get STDOUT
* stderr (bool): Get STDERR
* stream (bool): Return an iterator
* logs (bool): Get all previous output

**Returns** (generator or str): The logs or output for the image


## Tests

Unit tests are only provided for the pipeline, not the generic pipeline. They are in the unit_tests folder. Something to note is that a side effect of testing might be that a small busybox or alpine image remains on your machine.

## Contributors

James Audretsch: jamaudre@indiana.edu james.audretsch@cerner.com

## License
Still under consideration.
