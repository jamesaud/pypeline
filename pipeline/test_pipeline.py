import unittest
import os
from subprocess import call, Popen, PIPE
from pipeline.pipeline import Pipeline
from pipeline.image import Image

#This is a tricky, messy unit test because there are workspaces and docker images and containers created. It should all clean up by the end though.
#Every time an image or container is created, the id is manually added to a list and destroyed at the end.

#Common provids common methods for the unit tests
class Common:
    image_ids = []  # Image IDs to delete at test conclusion
    container_ids = []  # Container IDs to delete at test conclusion

    @classmethod
    def docker_item_exists(cls, id_num):  # Id num or name, something for docker inspect
        output = '_'
        with Popen('docker inspect --format="{{.Id}}" ' + id_num, shell=True, stdout=PIPE).stdout as stdout:
            output = stdout.read().strip()  # ID is the SHA256 Unique ID docker gives the image
        return True if (id_num in output) & (output != '') else False

    @classmethod
    def docker_tag_exists(cls, tag):  # Id num or name, something for docker inspect
        output = '_'
        with Popen('docker inspect ' + tag, shell=True, stdout=PIPE).stdout as stdout:
            output = stdout.read().strip()  # ID is the SHA256 Unique ID docker gives the image
        return True if (tag in output) & (output != '') else False

    @classmethod
    def addImageId(cls, id_num):
        Common.image_ids.append(id_num)

    @classmethod
    def addContainerID(cls, id_num):
        Common.container_ids.append(id_num)

    @classmethod
    def destroy(cls): #Destroy all the created images and containers
        if Common.container_ids:
            for id_num in set(Common.container_ids):
                call(['docker', 'rm', '-f', id_num])

        if Common.image_ids:
            for id_num in set(Common.image_ids):
                    call(['docker', 'rmi', '-f', id_num])

class PipelineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipe = Pipeline()
        cls.pipe.clone('https://github.com/jamesaud/simplest_docker') #Clone has to run before many of the other methods.
        #The dockerfile includes a barebones alpine image

    def test(self):
        self.assertEqual(4, 4)

    def test_clone(self):
        self.assertTrue(os.path.isdir(self.pipe.cloned_directory))

    def test_build(self):
        image = self.pipe.build()
        Common.addImageId(image.id)
        image2 = self.pipe.build('hello1203049')
        Common.addImageId(image2.id)
        image3 = self.pipe.build(directory='.')
        Common.addImageId(image3.id)
        self.assertTrue(Common.docker_item_exists(image.id))
        self.assertEqual('hello1203049', image2.name)
        self.assertTrue(Common.docker_tag_exists('hello1203049'))
        self.assertTrue(Common.docker_item_exists(image3.id))

    def test_pull(self):
        image = self.pipe.pull('alpine')
        Common.addImageId(image.id)
        image2 = self.pipe.pull('notadockerimage')
        Common.addImageId(image2.id)
        self.assertTrue(Common.docker_item_exists(image.id))
        self.assertFalse(Common.docker_item_exists(image2.id)) # It doesn't exist

    def test_close(self):
        self.pipe.close()
        self.assertFalse(os.path.isdir(self.pipe.work_directory))

    def test_with(self):
        with Pipeline() as newpipe:
            self.assertTrue(os.path.isdir(newpipe.work_directory)) #Tests if pipeline initalized
        self.assertFalse(os.path.isdir(newpipe.work_directory)) #Tests that pipeline deleted itself

    @classmethod
    def tearDownClass(cls): #Delete the junk folder, should happen in the test_close() method
        cls.pipe.close()
        Common.destroy()

#Build functionality is tested through the PipelineTest in test_build()
class ImageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls): #Run once for class
        cls.pipe = Pipeline()
        cls.pipe.pull('alpine').id

    def setUp(self):
        self.image = Image('alpine')
        Common.addImageId(self.image.id)

    def test_container(self):
        container1 = self.image.container()
        Common.addContainerID(container1.id)
        container2 = self.image.container('echo "hello world"') #This should run in the container, I don't know how to verify it.
        Common.addContainerID(container2.id)
        self.assertTrue(Common.docker_item_exists(container1.id))

    @classmethod
    def tearDownClass(cls): #Delete the workspace folder
        cls.pipe.close()
        Common.destroy()
        
#Run unit tests when calling script
if __name__ == "__main__":
    unittest.main()
    print("This test requires that docker daemon is installed and running.")
