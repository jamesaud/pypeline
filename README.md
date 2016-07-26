## Pypeline
A docker pipeline built in python. The ability to execute the following workflow:

*clone from github - build docker image - run tests in docker container(s) - push to docker repository*

## Code Examples
The **pipeline** module and **generic pipeline** module allow you to generate pipelines.
Please checkout the examples in 'examples' for full code.

### Pipeline
Create complex pipelines that allow for fast and flexible docker deployments.
```python
from pipeline import Pipeline

with Pipeline() as pipe:
    pipe.clone('https://github.cerner.com/JA048043/docker_test')  # clone from git
    test_image = pipe.build('justatest1232123/myawesomeimage')  # build with name
    test_image.run_container('echo "rspec"').remove()  # run commands in container, and delete.
    test_image.tag('justatest1232123/myawesomeimage', 'solid')  # Tag it with a solid name
    pipe.login(username='justatest1232123', password='Justatest123')  # Login to dockerhub
    test_image.push()  # Push.
    test_image.remove()  #Remove the image, if you really want.
```
However, it is possible to make the code much more compact.
```python
with Pipeline() as pipe:
        pipe.clone('https://github.cerner.com/JA048043/docker_test')
        with pipe.build() as myImage, myImage.run_container('echo "unit-tests"'):
            myImage.tag("dockerhub.cerner.com/jamesaudretsch/myawesomeimage").push('latest')
#  The image and container are automatically deleted when the block ends.
```

### Generic Pipeline
The easiest but less flexible way to build a pipeline. The goal of the Generic Pipeline is to streamline the process for testing on a single image.

```python
with GenericPipeline() as GP:
        GP.build('https://github.com/jamesaud/simplest_docker')  # Clone and build.
        GP.test('echo "first test"', 'echo "second test"', 'echo "third test"')  # Run parallel commands in separate containers
        GP.login(username='justatest1232123', password='Justatest123')  # Optional registry argument
        GP.push('latest')  # Tag before it pushes.
```
## Motivation

A short description of the motivation behind the creation and maintenance of the project. This should explain **why** the project exists.

## Installation

Provide code examples and explanations of how to get the project.

## API Reference

Depending on the size of the project, if it is small and simple enough the reference docs can be added to the README. For medium size to larger projects it is important to at least provide a link to where the API reference docs live.

## Tests

Describe and show how to run the tests with code examples.

## Contributors

Let people know how they can dive into the project, include important links to things like issue trackers, irc, twitter accounts if applicable.

## License

A short snippet describing the license (MIT, Apache, etc.)
