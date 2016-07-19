# pypeline
a docker pipeline in python - clone from git, build docker image, run tests in docker containers, push to docker repo.

#Installation
clone:
>git clone https://github.cerner.com/JA048043/pypeline

install (make sure pip is installed):
>cd pypeline

>sudo python3 setup.py install

Copy the code from 'example_pipe.py' and see how it works.

# Use
- Currently, you must do the full import to run the code. Open a python3.5 file and write:
>from pypeline.pipeline.pipeline import Pipeline

- Create Pipeline object:
> pipe = Pipeline()

> pipe.close()
- You must close the Pipeline object at the end, so preferably use 'with' instead. It will automatically close at the end of the block:
>with Pipeline() as pipe:
>    ...

- Make a docker image:
Pull an image:
>image = pipe.pull('alpine:latest')
- Delete an image:
>image.remove()

- Or, Clone and Build an image (optional path to dockerfile argument):
>pipe.clone('https://github.com/jamesaud/simplest_docker')
>image = pipe.build()

- Image supports the 'with' syntax as well:
>with pipe.pull('alpine:latest') as alpine_image:
>    ...

- Run a container based on an image
>container = image.container('echo "hello world!")
- Remove a container
>container.remove()

- Container supports 'with' syntax:
>with alpine_image.container('echo "hello world"'):
>    ...:

- Push an image to dockerhub
Tag an image:
>alpine_newest = alpine_image.tag('superawesomealpine', 'version1')

- Login to dockerhub:
>pipe.login(username='myName', password='secret')

- Push the image:
>alpine_newest.push()