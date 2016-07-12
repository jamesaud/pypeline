# pypeline
a docker pipeline in python

I haven't written all the tests yet. Use cases are in example.py. Clone and run example_pipe.py and example_rails.py to see it in action.
example_rails.py automates the pipeline process specifically for rails apps.

There is still a lot to be done including many more tests and login credentials for dockerhub

Clone the repository, and run 'example_pipe.py' or 'example_rails.py' to see how it works. 

example_pipe - the generic version of a pipeline that you can build, with several example use cases.

example_rails - a specialized verison build for rails apps. The goal is do not require developers to have a Dockerfile in their project. Expands using the workflow/rails module.
