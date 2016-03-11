"""Manages the lifecycle of a docker container.

Use via the with statement:

with Container(some_image) as c:
    for line in c.run("some_command"):
        print line
"""
import docker
import click, os


# sets the docker host from your environment variables
client = docker.Client(
    **docker.utils.kwargs_from_env(assert_hostname=False))


class Container:
    """
    Represents a single docker container on the host.
    
    Volumes should be a list of mapped paths, e.g. ['/var/log/docker:/var/log/docker'].
    """

    def __init__(self, image, memory_limit_gb=4, stderr=True, stdout=True, volumes=[], cleanup=True):
        self.image = image
        self.memory_limit_bytes = int(memory_limit_gb * 1e9)
        self.stderr = stderr
        self.stdout = stdout
        self.volumes = [x[1] for x in map(lambda vol: vol.split(':'), volumes)]
        self.binds = volumes
        self.cleanup = cleanup

    def __enter__(self):
        """Power on."""
        self.container_id = client.create_container(
            image=self.image,
            volumes=self.volumes,
            host_config=client.create_host_config(
                mem_limit=self.memory_limit_bytes,
                binds=self.binds
                ),
            stdin_open=True
        )['Id']

        client.start(self.container_id)

        return self

    def __exit__(self, type, value, traceback):
        """Power off."""
        client.stop(self.container_id)
        if self.cleanup:
            client.remove_container(self.container_id)

    def run(self, command):
        """Just like 'docker run CMD'.

        This is a generator that yields lines of container output.
        """
        exec_id = client.exec_create(
            container=self.container_id,
            cmd=command,
            stdout=self.stdout,
            stderr=self.stderr
        )['Id']

        for line in client.exec_start(exec_id, stream=True):
            yield line


@click.command()
@click.argument('do', nargs=-1)
@click.option('--image', help='Image name in which to run do', default=None)
@click.option('--sharedir', help='Directory on host machine to mount to docker.', default=os.path.abspath(os.getcwd()))
def dodo(do, image, sharedir):
    """ dodo (like sudo but for docker) runs argument in a docker image.

    do is the argument to execute in image.
    image is set as "DODOIMAGE" environment variable.
    sharedir (e.g., to pass data to command) is mounted (default: current directory).
    """

    if not image:
        try:
            image = os.environ['DODOIMAGE']
        except KeyError:
            print('No image provided or available as DODOIMAGE environment variable.')
            raise

    volumes = ['{}:/home'.format(sharedir)]

    print('In {}, running: {}'.format(image, ' '.join(do)))

    with Container(image, volumes=volumes) as c:
        for output_line in c.run(do):
            print(output_line)
