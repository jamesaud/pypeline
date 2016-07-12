import config.docker_client as dc


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

