import docker

RAILS_DOCKERFILE_LOCATION = 'data/rails/Dockerfile'

DOCKER_CLIENT = docker.from_env(assert_hostname=False)

REPOSITORY = 'dockerhub.com'