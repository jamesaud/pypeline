from pipeline.pipeline import Pipeline

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
    Notes - the image used in this test might fail to delete if it already has dependent images on your machine.
    """
    """
    Good way to run a pipeline.
    """
    with Pipeline() as pipe:  # Cleans up (deletes work_directory) automatically at the end of the block.
        pipe.clone('https://github.cerner.com/JA048043/docker_test')
        test_image = pipe.build()  # Build image, optional name, optional directory path: pipe.build("myImgName", directory="dockerstuff")
        with test_image.container('sleep 6') as container1:  # Run container with optional command. Automatically deletes container at the end of the block.
            container1.inside('echo "hello There!"')  # Run command in running container. If the container's not running, it will error!
        test_image.tag('dockerhub.cerner.com/jamesaudretsch/myawesomeimage', 'solid')  # Tag it with a solid name
        test_image.push()
        #test_image.remove()  #Remove the image, if you really want.



    """
    A shorter way to achieve the same results
    """
    with Pipeline() as pipe:
        pipe.clone('https://github.cerner.com/JA048043/docker_test')
        with pipe.build() as myImage, myImage.container('sleep 6') as container1:  #Image removes itself, container removes itself.
            container1.inside('echo "hello There!"')
            myImage.tag("dockerhub.cerner.com/jamesaudretsch/myawesomeimage").push()  # If you don't give it a tag, it defaults to latest



    """
    The shortest way to achieve the same results.
    """
    with Pipeline() as pipe, pipe.pull('busybox') as myImage, myImage.container('echo "rspec"'):
        myImage.tag("dockerhub.cerner.com/jamesaudretsch/myawesomeimage", "latest").push()



    """
    The bad way to do this, but is useful in some cases.
    """
    pipe = Pipeline()
    test_image = pipe.pull('busybox')  # Pull image
    test_image.remove()
    pipe.clone('https://github.cerner.com/JA048043/docker_test')  # Clone from git
    test_image = pipe.build('myawesomeimage')  # Build image, optional directory path as second argument.
    container1 = test_image.container('sleep 6')  # Run container with optional command
    container1.inside('echo "hello There!"')  # Run command in running container. If the containers not running, it gives the error.
    container1.remove()  # Destroy container
    #test_image.remove() #optionally remove the image
    pipe.close() #Clean up


if __name__ == "__main__":
    test()
