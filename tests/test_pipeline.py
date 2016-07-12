from pipeline.pipeline import Pipeline
import unittest
import tests.test_dc as tdc
import config.docker_client as dc
import os


# This is a tricky, messy unit test because there are workspaces and docker images and containers created. It should all clean up by the end though.
# Every time an image or container is created, the id is manually added to a list and destroyed at the end.

"""
class PipelineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipe = Pipeline()
        cls.pipe.clone(
            'https://github.com/jamesaud/simplest_docker')  # Clone has to run before many of the other methods.
        # The dockerfile includes a barebones alpine image

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
        self.assertFalse(Common.docker_item_exists(image2.id))  # It doesn't exist

    def test_close(self):
        self.pipe.close()
        self.assertFalse(os.path.isdir(self.pipe.work_directory))

    def test_with(self):
        with Pipeline() as newpipe:
            self.assertTrue(os.path.isdir(newpipe.work_directory))  # Tests if pipeline initalized
        self.assertFalse(os.path.isdir(newpipe.work_directory))  # Tests that pipeline deleted itself

    @classmethod
    def tearDownClass(cls):  # Delete the junk folder, should happen in the test_close() method
        cls.pipe.close()
        Common.destroy()

"""
# Build functionality is tested through the PipelineTest in test_build()
class ImageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # Run once for class
        cls.pipe = Pipeline()
        cls.image = cls.pipe.pull('busybox')

    def test_container(self):
        with self.image.container() as container1:
            cont1_id = container1.id
            self.assertTrue(tdc.container_exists(container1.id)) # Assert it exists
        self.assertFalse(tdc.container_exists(cont1_id)) # Assert it is automatically destroyed
        with self.image.container('echo "hello world"') as container2: # This should run in the container, I don't know how to verify it.
            self.assertTrue(tdc.container_exists(container2.id))

    def test_tag(self):
        repo, tagged = 'my.repo.com/james', 'newest'
        self.image.tag(repo, tagged)
        self.assertIn(repo + ':' + tagged, dc.find_image(self.image.id)['RepoTags'])

    @classmethod
    def tearDownClass(cls):  # Delete the workspace folder
        cls.image.remove()
        cls.pipe.close()

class TestPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipe = Pipeline()
        cls.pipe.clone('https://github.com/jamesaud/simplest_docker')  # Clone has to run before many of the other methods.
        # The dockerfile includes a barebones alpine image

    @classmethod
    def tearDownClass(cls):  # Delete the junk folder, should happen in the test_close() method
        cls.pipe.close()

    def test_clone(self):
        self.assertTrue(os.path.isdir(self.pipe.cloned_directory))

    def x_test__changeToClonedDirAndExecute(self):
        def simple_write():
            with open("test23432.txt", 'w')as test_file:
                test_file.write('....')

        self.pipe._changeToClonedDirAndExecute(simple_write)
        self.assertTrue("test23432" in self.pipe.cloned_directory.listdir())


    def test_build(self):
        with self.pipe.build() as image:
            self.assertTrue(tdc.image_exists(image.id))
        self.assertFalse(tdc.image_exists(image.id))   # Make sure image auto destroys itself

        with self.pipe.build('hello1203049') as image2: # Test assign name to image, need to test further
            self.assertEqual('hello1203049', image2.name)
            self.assertTrue(tdc.image_exists(image2.id))

        with self.pipe.build(directory='.') as image3: # Test build path, need to test further
            self.assertTrue(tdc.image_exists(image3.id))

        #self.assertTrue(Common.docker_tag_exists('hello1203049'))

    def test_pull(self):
        with self.pipe.pull('busybox') as image:
            self.assertTrue(tdc.image_exists(image.id))

        try:
            image2 = self.pipe.pull('notadockerimage')
        except:
            image2 = False # Image2 failed to create
        self.assertFalse(image2)

    def test_copyToClonedDirectory(self):
        pass

    def test_with(self):
        with Pipeline() as newpipe:
            self.assertTrue(os.path.isdir(newpipe.work_directory))  # Tests if pipeline initalized
        self.assertFalse(os.path.isdir(newpipe.work_directory))  # Tests that pipeline deleted itself

    def test_close(self):
        newpipe = Pipeline()
        newpipe.close()
        self.assertFalse(os.path.isdir(newpipe.work_directory))


# Run unit tests when calling script
if __name__ == "__main__":
    unittest.main()
    print("This test requires that docker daemon is installed and running.")
