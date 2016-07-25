import docker
import docker.tls as docker_tls
import os
import logging

"""
Set configuration in init.py.
"""

CLIENT = None
DEFAULT_REGISTRY = 'https://index.docker.io/v1/'
LOGGING_LEVEL = logging.INFO

def _set_logger():
    # Set the logger to log info to stdout
    logging.basicConfig(level=LOGGING_LEVEL, format='%(message)s')


def setup(DOCKER_BASE_URL='https://192.168.99.100:2376',
          CERTS=os.path.join(os.path.expanduser('~'), '.docker', 'machine', 'machines', 'default'),
          TLS=None):
    """
    Setup the docker machine.
    :param docker_base_url: Str - url of the docker machine
    :param certs_path: Str - path of the certs.
    :param TLS: Dict: required keys: {client_cert: Str, ca_cert: Str, verify: Bool} - custom keys.
    :return:
    - note - refer to the dockerpy documentation.
    """
    global CLIENT

    if TLS is None:
        client_cert = os.path.join(CERTS, 'cert.pem'), os.path.join(CERTS, 'key.pem')
        ca_cert = os.path.join(CERTS, 'ca.pem')
        verify = True
    else:
        client_cert = TLS['client_cert']
        ca_cert = TLS['ca_cert']
        verify = TLS['verify']

    TLS_CONFIG = docker_tls.TLSConfig(
        client_cert=client_cert,
        ca_cert=ca_cert,
        verify=verify)

    CLIENT = docker.Client(base_url=DOCKER_BASE_URL, tls=TLS_CONFIG)