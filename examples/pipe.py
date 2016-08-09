from pypeline.pipeline import Pipeline
from pypeline.config import clientsetup
#------The good way to do this------
def test():
    """
    Runs a basic pipeline.
    Each block of code runs a new pipeline.
    ---Steps---
    1. Clone image from github.
    2. Build image.
    3. Start container and run code(tests?) inside.
    4. Tag image with nice name.
    5. Push image to repository.
    -----------
    """

    """
    Good way to run a pipeline.
    """
    clientsetup(default=True, docker_base_url='https://192.168.99.100:2376')
    with Pipeline() as pipe:  # Cleans up (deletes work_directory) automatically at the end of the block.
        pipe.clone('https://github.com/jamesaud/simplest_docker')
        test_image = pipe.build()  # Build image, optional name, optional directory path: pipe.build("myImgName", path="dockerstuff")
        test_image.container('sleep 6').remove()  # Run container with optional command. delete container after.
        test_image.tag('justatest1232123/myawesomeimage:solid')  # Tag it with a solid name
        pipe.login(username='justatest1232123', password='Justatest123')  # Login to dockerhub
        test_image.push()
        #test_image.remove()  #Remove the image, if you really want.



    """
    A shorter way to achieve the same results
    """
    with Pipeline() as pipe:
        pipe.clone('https://github.com/jamesaud/simplest_docker')
        with pipe.build() as myImage, myImage.run_container('sleep 6'):  # Image removes itself, container removes itself.
            myImage.tag("jamesaudretsch/myawesomeimage").push()  # If you don't give it a tag, it defaults to latest



    """
    The shortest way to achieve the same results.
    With an example of logging in to dockerhub.com
    """
    with Pipeline() as pipe, pipe.pull('alpine:latest') as myImage, myImage.run_container(args='echo "rspec"'):
        pipe.login(username='justatest1232123', password='Justatest123')  # Login to dockerhub
        myImage.tag("justatest1232123/myawesomeimage:jusatest").push()



    """
    The bad way to do this, but is useful in some cases.
    """
    pipe = Pipeline()
    test_image = pipe.pull('busybox')  # Pull image
    test_image.remove()  # Remove image
    pipe.clone('https://github.com/jamesaud/simplest_docker')  # Clone from git
    test_image = pipe.build('myawesomeimage')  # Build image, optional directory path as second argument.
    container1 = test_image.container(args='sleep 6', name='myawesomecontainer')  # Create container, optional name
    container1.run()  # Run container
    container1.remove()  # Destroy container
    #test_image.remove() #optionally remove the image
    pipe.close() #Clean up

    """
    Run containers in parallel.
    """
    with Pipeline() as pipe:
        img = pipe.pull('busybox:latest')
        # Takes commands as arguments, and runs each comma separated one in a separate container.
        img.run_parallel_containers('echo "rspec spec"', 'echo "hello world"')


if __name__ == "__main__":
    test()
