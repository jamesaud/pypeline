import docker
import os
import logging
import docker.tls as tls


DOCKER_MACHINE_IP = '192.168.99.100'
DOCKER_CLIENT = None
RAILS_DOCKERFILE_LOCATION = 'data/rails/Dockerfile'


def setup():
    global DOCKER_CLIENT
    CERTS = os.path.join(os.path.expanduser('~'), '.docker', 'machine', 'machines', 'default')
    TLS_CONFIG = tls.TLSConfig(
        client_cert=(os.path.join(CERTS, 'cert.pem'), os.path.join(CERTS, 'key.pem')),
        ca_cert=os.path.join(CERTS, 'ca.pem'),
        verify=True)

    DOCKER_CLIENT = docker.Client(base_url='https://{}:2376'.format(DOCKER_MACHINE_IP), tls=TLS_CONFIG)
    # DOCKER_CLIENT = docker.from_env(assert_hostname=False)

    # Set the logger to log info to stdout
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')