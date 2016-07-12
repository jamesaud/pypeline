import docker

RAILS_DOCKERFILE_LOCATION = 'data/rails/Dockerfile'

DOCKER_CLIENT = docker.from_env(assert_hostname=False)

REPOSITORY = 'dockerhub.com'

DOCKER_MACHINE_IP = '192.168.99.100'
