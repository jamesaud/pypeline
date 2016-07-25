from pypeline.pipeline import Pipeline

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
    Notes - the images used in this example might fail to delete if it already has dependent images on your machine.
    """
    """
    Good way to run a pipeline.
    """
    with Pipeline() as pipe:  # Cleans up (deletes work_directory) automatically at the end of the block.
        pipe.clone('https://github.cerner.com/JA048043/docker_test')
        test_image = pipe.build()  # Build image, optional name, optional directory path: pipe.build("myImgName", path="dockerstuff")
        test_image.container('sleep 6').remove()  # Run container with optional command. delete container after.
        test_image.tag('justatest1232123/myawesomeimage', 'solid')  # Tag it with a solid name
        pipe.login(username='justatest1232123', password='Justatest123')  # Login to dockerhub
        test_image.push()
        #test_image.remove()  #Remove the image, if you really want.



    """
    A shorter way to achieve the same results
    """
    with Pipeline() as pipe:
        pipe.clone('https://github.cerner.com/JA048043/docker_test')
        with pipe.build() as myImage, myImage.run_container('sleep 6'):  # Image removes itself, container removes itself.
            myImage.tag("dockerhub.cerner.com/jamesaudretsch/myawesomeimage").push()  # If you don't give it a tag, it defaults to latest



    """
    The shortest way to achieve the same results.
    With an example of logging in to dockerhub.com
    """
    with Pipeline() as pipe, pipe.pull('alpine:latest') as myImage, myImage.run_container('echo "rspec"'):
        pipe.login(username='justatest1232123', password='Justatest123')  # Login to dockerhub
        myImage.tag("justatest1232123/myawesomeimage", "jusatest").push()



    """
    The bad way to do this, but is useful in some cases.
    """
    pipe = Pipeline()
    test_image = pipe.pull('busybox')  # Pull image
    test_image.remove()
    pipe.clone('https://github.cerner.com/JA048043/docker_test')  # Clone from git
    test_image = pipe.build('myawesomeimage',)  # Build image, optional directory path as second argument.
    container1 = test_image.container('sleep 6')  # Create container with optional command
    container1.run()  # Run container
    container1.remove()  # Destroy container
    #test_image.remove() #optionally remove the image
    pipe.close() #Clean up

    """
    Run containers in parallel.
    """
    with Pipeline() as pipe:
        img = pipe.pull('busybox:latest')
        # Takes containers as arguments.
        img.run_parallel_containers('echo "rspec spec"', 'echo "hello world"')


if __name__ == "__main__":
    test()
