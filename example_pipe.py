from pipeline.pipeline import Pipeline

#------The good way to do this------
def test():
    with Pipeline() as pipe: # Cleans up (deletes work_directory) automatically at the end of the block
        test = pipe.pull('busybox') # You can pull the image
        test.remove()  # Removed the image
        #or you can clone from git and build...
        pipe.clone('https://github.cerner.com/JA048043/docker_test')
        test_image = pipe.build()  #Build image, optional name, optional directory path.
        #Could be: pipe.build("myImgName", directory="dockerstuff")

        with test_image.container('sleep 6') as container1:  # Run container with optional command. Automatically deletes container at the end of the block.
            container1.inside('echo "hello There!"')  # Run command in running container. If the container's not running, it will error.
        test_image.tag('dockerhub.cerner.com/jamesaudretsch/myawesomeimage', 'newest')  # Tag it with a solid name
        test_image.push()
        #test_image.remove() #Remove the image, if you really want.

    #Or it could get even simpler!
    with Pipeline() as pipe:
        pipe.clone('https://github.cerner.com/JA048043/docker_test')
        with pipe.build() as myImage, myImage.container('sleep 6') as container1: #Image removes itself, container removes itself.
            container1.inside('echo "hello There!"')
            myImage.tag("dockerhub.cerner.com/jamesaudretsch/myawesomeimage").push()  # Or if you don't tag it, it defaults to latest

    #Or even simpler, if you don't have to clone. Python evaluates as nested 'with's. Maybe two lines IS execssively short:
    with Pipeline() as pipe, pipe.pull('busybox') as myImage, myImage.container('sleep 6') as container1:
        myImage.tag("dockerhub.cerner.com/jamesaudretsch/myawesomeimage").push() if container1.inside('echo "hello There!"') else None


    #-----The bad way to do this, but could be useful in some cases------
    pipe = Pipeline()
    test_image = pipe.pull('busybox')  # Pull image
    #or clone from git and build...
    pipe.clone('https://github.cerner.com/JA048043/docker_test') #Clone from git
    test_image = pipe.build('myawesomeimage') #Build image, optional directory path as second argument.
    container1 = test_image.container('sleep 6') #Run container with optional command
    container1.inside('echo "hello There!"') #Run command in running container. If the containers not running, it gives the error.
    container1.remove() #Destroy container
    #test_image.remove() #optionally remove the image
    pipe.close() #Clean up

  #  with Pipeline() as pipe:
  #      img = pipe.pull('busybox')
  #      with img.container('sleep 100') as cont:
  #          cont.inside('echo "hello worl world -----------"')

if __name__ == "__main__":
    test()
