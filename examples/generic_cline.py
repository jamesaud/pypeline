#!/usr/bin/python

import sys
import re
from datetime import datetime
from pypeline.generic_pipeline import GenericPipeline
from pypeline.config import clientsetup


def stage(name):
    print("\n----- {} -----\n".format(name) + "-" * 27 + "\n")


def tag_with_time():
    return datetime.now().utcnow().strftime('%Y-%m-%d--%Hh%Mm%Ss')


def run(registry, registry_username, registry_password, git_url, repository, *test):
    print(registry + '\n\n\n')
    """
    Using an alpine image.
    """
    clientsetup(default=True, docker_base_url='https://192.168.99.100:2376')
    with GenericPipeline() as GP:
        stage('Clone and Build')
        GP.build(git_url)  # Optional dockerfile directory and dockerfile name
        stage("Test")
        GP.test(*test)  # Run parallel commands in separate containers
        stage("Push")
        GP.login(username=registry_username, password=registry_password, registry=registry, repository=repository)  # Optional registry argument
        GP.push(tag_with_time())  # Tag before it pushes, defaults to latest with no argument


if __name__ == "__main__":
    # Validation to make sure that the arguments are entered correctly.
    args = {'registry': None, 'username': None, 'password': None, 'url': None, 'repository' : None, 'test': []}
    res = re.findall('--[^--]*', ' '.join(sys.argv[1:]) + ' ')
    for item in res:
        try:
            data = re.findall('[^ ]* ', item[2:])
            keyword = data[0].strip()
            value = ''.join(data[1:]).strip()
        except:
            raise ValueError('Invalid argument', item)
        else:
            if keyword == 'test':
                args['test'].append(value)
            else:
                args[keyword] = value
    print('\n\n\n\n')
    print(args)
    run(args['registry'], args['username'], args['password'], args['url'], args['repository'], *args['test'])
