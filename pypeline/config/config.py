import docker
import docker.tls as docker_tls
import os
import logging
from .docker_client import DockerClient

"""
Set configuration in init.py.
"""

DEFAULT_REGISTRY = 'https://index.docker.io/v1/'
LOGGING_LEVEL = logging.INFO


def _set_logger():
    # Set the logger to log info to stdout
    logging.basicConfig(level=LOGGING_LEVEL, format='%(message)s')


def clientsetup(docker_base_url=None,
          TLS=None,
          default=False):
    """
    Setup the docker machine.
    :param docker_base_url: Str - url of the docker machine
    :param certs_path: Str - path of the certs.
    :param TLS: Dict: required keys: {client_cert: Str, ca_cert: Str, verify: Bool} - custom keys.
    :return: None
    - note - refer to the dockerpy documentation.
    """
    global CLIENT
    global TSL_CONFIG

    if default:
        CERTS = os.path.join(os.path.expanduser('~'), '.docker', 'machine', 'machines', 'default')

        TLS_CONFIG = docker_tls.TLSConfig(
            client_cert = (os.path.join(CERTS, 'cert.pem'), os.path.join(CERTS, 'key.pem')),
            ca_cert = os.path.join(CERTS, 'ca.pem'),
            verify = True)
    else:
        if TLS:
            TLS_CONFIG = docker_tls.TLSConfig(
            client_cert=TLS['client_cert'],
            ca_cert=TLS['ca_cert'],
            verify=TLS['verify'])
        else:
            TLS_CONFIG = None

    CLIENT = docker.Client(base_url=docker_base_url, tls=TLS_CONFIG)
    DockerClient.assign_client(CLIENT)
    _set_logger()
