from workflow.rails.railspipeline import RailsPipeline


def stage(name):
    print("\n----- {} -----\n".format(name) + "-" * 30 + "\n")


def test():
    with RailsPipeline('https://github.cerner.com/JA048043/r_wellness', 'dockerhub.cerner.com') as rp:
        stage("Clone")
        rp.clone()
        stage("Build")
        rp.build()
        stage("Test")
        rp.test('rspec spec', 'echo "hello world"')  # Eventually this command will run in the same container.
        # rp.test('rspec spec')                       # And this command will run a parallel container.
        stage("Push")
        rp.push('newest')  # Tag before it pushes, defaults to latest with no argument


if __name__ == "__main__":
    test()