import os
import unittest

from pypeline.config.docker_client import DockerClient as dc

import pypeline.unit_tests.test_helper as th
from pypeline.pipeline.pipeline import Pipeline
from pypeline.config.config import clientsetup
"""
This is a tricky, messy unit test because there are workspaces and docker images and containers created.
It should all (mostly?) clean up by the end though, and uses busybox image to maintain fast test speeds.
Can't delete busybox image in case it's already on the user's hard drive.
"""


class Image_And_Container_Test(unittest.TestCase):
    """ Test image and container classes. """
    @classmethod
    def setUpClass(cls):  # Run once for class
        """ Creates a pipeline and pulls a busybox image """
        clientsetup(default=True, docker_base_url='https://192.168.99.100:2376')
        cls.pipe = Pipeline()
        cls.image = cls.pipe.pull('busybox:latest')

    def test_run_container(self):
        """ Should create a container from an image """
        with self.image.run_container() as container1:
            cont1_id = container1.id
            self.assertTrue(th.container_exists(container1.id))  # Assert it exists
        self.assertFalse(th.container_exists(cont1_id))  # Assert it is automatically destroyed
        with self.image.run_container('echo "hello world"') as container2:  # This should run in the container, I don't know how to verify it.
            self.assertTrue(th.container_exists(container2.id))

    def test_create_container(self):
        with self.image.container('echo "hello"') as container1:
            container1.run()
            self.assertTrue(th.container_exists(container1.id))

    def test_tag(self):
        """ Should add a tag to an image """
        tagged= 'my.repo.com/james:newest'
        self.image.tag(tagged)
        self.assertIn(tagged, dc.find_image(self.image.name)['RepoTags'])


    @classmethod
    def tearDownClass(cls):
        """ Delete the pipeline workspace """
        cls.pipe.close()

class TestPipeline(unittest.TestCase):
    """ Test pipeline class """
    @classmethod
    def setUpClass(cls):
        """ Creates a pipeline and clones a dockerfile repo from github """
        clientsetup(default=True, docker_base_url='https://192.168.99.100:2376')
        cls.pipe = Pipeline()
        cls.pipe.clone('https://github.com/jamesaud/simplest_docker')  # Clone has to run before many of the other methods.
        # The dockerfile includes a barebones alpine image

    @classmethod
    def tearDownClass(cls):
        """ Should delete the pipeline workspace """
        cls.pipe.close()

    def test_clone(self):
        """ Verify clone from git from setUpClass() """
        self.assertTrue(os.path.isdir(self.pipe.cloned_directory))

    def test_copy_to_cloned_directory(self):
        """ Should copy a file to the cloned directory """
        filename = 'test23432.txt'
        with open(filename, 'w')as test_file:
            test_file.write('....')
        file_path = os.path.join(os.getcwd(), filename)
        self.pipe.copy_to_cloned_directory(file_path)
        self.assertTrue(filename in os.listdir(self.pipe.cloned_directory))
        os.remove(file_path)

    def test_build(self):
        """ Should build an image """
        with self.pipe.build() as image:  # Build image
            self.assertTrue(th.image_exists(image.name))
        self.assertFalse(th.image_exists(image.name))  # Make sure image auto destroys itself

        with self.pipe.build('hello1203049') as image2:  # Build image with tag
            self.assertEqual('hello1203049', image2.name)
            self.assertTrue(th.image_exists(image2.name))

        with self.pipe.build(path='.') as image3:  # Build image in build path. Needs to be more extensive.
            self.assertTrue(th.image_exists(image3.name))

    def test_pull(self):
        """ Should pull an image """
        image = self.pipe.pull('busybox:latest')  # Pull image
        self.assertTrue(th.image_exists(image.name))

        try:
            image2 = self.pipe.pull('notadockerimage')  # Pull image that doesn't exist - should error.
        except:
            image2 = False  # Image2 failed to create
        self.assertFalse(image2)

    def test_with(self):
        """ Should work with 'with' functionality """
        with Pipeline() as newpipe:  # Should delete pipeline workspace automatically.
            self.assertTrue(os.path.isdir(newpipe.work_directory))   # Tests if pipeline initialized
        self.assertFalse(os.path.isdir(newpipe.work_directory))   # Tests that pipeline deleted itself

    def test_close(self):
        """ Should delete the pipeline workspace """
        newpipe = Pipeline()
        newpipe.close()
        self.assertFalse(os.path.isdir(newpipe.work_directory))


# Run unit tests when calling script
if __name__ == "__main__":
    unittest.main()
    print("This test requires that docker daemon is installed and running.")
