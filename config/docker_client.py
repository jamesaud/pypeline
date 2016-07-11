import docker
import os

cli = docker.from_env(assert_hostname=False)


def pull(image_name):
    for line in cli.pull(image_name, stream=True):
        print(line)

# Find by image id
def find_image(image_id):
    return cli.inspect_image(image_id)


def find_image_by_name(image_name):
    return cli.images(image_name)


def find_container(container_id):
    return cli.inspect_container(container_id)


def remove_image(image): #id or name
    cli.remove_image(image, True)
    print("removed image:", image)


def remove_container(container):
    cli.remove_container(container, True)
    print("removed container :", container)


def build(dockerfile_path, image_name):
    print("building image", image_name)
    print(os.listdir(os.getcwd()))
    for line in cli.build(path=dockerfile_path, rm=True, tag=image_name):
        print(line)

def push(push_url):
    for line in cli.push(push_url, stream=True):
        print(line)

