import config.docker_client as dc

"""
Helper functions for unit tests.
"""


def image_exists(image_name):
    if dc.find_image_by_name(image_name):
        return True
    else:
        return False


def container_exists(container_id):
    try:
        dc.find_container(container_id)
        return True
    except:
        return False

