from pypeline.generic_pipeline import GenericPipeline
from pypeline.config import clientsetup
from datetime import datetime

"""
Examples of using the GenericPipeline.
Using the 'with' syntax is preferred. If you forget to close the pipeline,
a directory will remain in your machines current directory.
"""


def stage(name):
    print("\n----- {} -----\n".format(name) + "-" * 27 + "\n")


def tag_with_time():
    return datetime.now().utcnow().strftime('%Y-%m-%d--%Hh%Mm%SsUTC')


def test():
    """
    Using an alpine image.
    """
    clientsetup(default=True, docker_base_url='https://192.168.99.100:2376')

    with GenericPipeline() as GP:
        stage('Clone and Build')
        GP.build('https://github.com/jamesaud/simplest_docker')  # Optional dockerfile directory and dockerfile name
        stage("Test")
        GP.test('echo "first test"', 'echo "second test"', 'echo "third test"')  # Run parallel commands in separate containers
        stage("Push")
        GP.login(username='justatest1232123', password='Justatest123')  # Optional registry argument
        GP.push(tag_with_time())  # Tag before it pushes, defaults to latest with no argument


def test2():
    """
    Using a rails app.
    Alternative syntax. If you forget to close, the git cloned work directory will be left in your current directory.
    """
    clientsetup(default=True, docker_base_url='https://192.168.99.100:2376')

    RP = GenericPipeline()
    try:
        RP.login(registry='dockerhub.cerner.com/', repository='jamesaudretsch')
        stage("Clone and Build")
        RP.build('https://github.cerner.com/JA048043/r_wellness')
        stage("Test")
        RP.test('rspec spec', 'rspec spec', 'echo "third test"')  # Run parallel tests in separate containers
        stage("Push")
        RP.push('latest')
    finally:  # Make sure to cleanup on an error. 'with' syntax is preferred.
        RP.close()


if __name__ == "__main__":
    print('\n\n{}\nEXAMPLE 1 -------------\n{}'.format('-' * 23, '-' * 23))
    test()
    print('\n\n{}\nEXAMPLE 2 -------------\n{}'.format('-' * 23, '-' * 23))
    test2()
