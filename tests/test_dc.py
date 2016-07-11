import unittest
import os
from subprocess import call, Popen, PIPE
from pipeline.pipeline import Pipeline
from pipeline.image import Image
import config.docker_client as dc
import docker

def image_exists(image_id):
    try:
        dc.find_image(image_id)
        return True
    except:
        return False


def container_exists(container_id):
    try:
        dc.find_container(container_id)
        return True
    except:
        return False

