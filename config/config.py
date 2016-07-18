import docker
import os
import logging
import docker.tls as tls

CERTS = os.path.join(os.path.expanduser('~'), '.docker', 'machine', 'machines', 'default')
docker_machine_ip = '192.168.99.100'
tls_config = tls.TLSConfig(
    client_cert=(os.path.join(CERTS, 'cert.pem'), os.path.join(CERTS, 'key.pem')),
    ca_cert=os.path.join(CERTS, 'ca.pem'),
    verify=True)


DOCKER_CLIENT = docker.Client(base_url='https://{}:2376'.format(docker_machine_ip), tls=tls_config) #DOCKER_CLIENT = docker.from_env(assert_hostname=False)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

RAILS_DOCKERFILE_LOCATION = 'data/rails/Dockerfile'

DOCKER_MACHINE_IP = '192.168.99.100'