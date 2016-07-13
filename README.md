# pypeline
a docker pipeline in python - clone from git, build docker image, run tests in docker containers, push to docker repo.

I've written many but not all the tests yet. There is still a lot to be done.

Clone the repository, and run 'example_pipe.py' or 'example_rails.py' to see how it works. 

example_pipe - the generic version of a pipeline that you can build, with several example use cases.

example_rails - a specialized verison build for rails apps. The goal is to not require developers to have a Dockerfile in their project. Expands using the workflow/rails module.

