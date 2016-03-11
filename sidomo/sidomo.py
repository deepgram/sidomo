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

    def __init__(self, image, memory_limit_gb=4, stderr=True, stdout=True, volumes=[], cleanup=False):
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
@click.option('--image', '-i', help='Image name in which to run do', default=None)
@click.option('--sharedir', '-s', help='Directory on host machine to mount to docker.', default=os.path.abspath(os.getcwd()))
def dodo(do, image, sharedir):
    """ dodo (like sudo but for docker) runs argument in a docker image.

    do is the command to run in the image.
    image taken from (1) command-line, (2) "DODOIMAGE" environment variable, or (3) first built image.
    sharedir (e.g., to pass data to command) is mounted (default: current directory). empty string does no mounting.
    """

    # try to set image three ways
    if not image:
        if 'DODOIMAGE' in os.environ:
            image = os.environ['DODOIMAGE']
        else:
            ims = client.images()
            if len(ims) >= 1:
                image = [im['RepoTags'][0] for im in client.images()][0]

    assert image, 'No image given or found locally.'

    # get image if not available locally
    imnames = [im['RepoTags'][0] for im in client.images()]
    if (not any([image in imname for imname in imnames])) and client.search(image):
        print('Image {} not found locally. Pulling from docker hub.'.format(image))
        client.pull(image)

    if sharedir:
        volumes = ['{}:/home'.format(sharedir)]
    else:
        volumes = []

    with Container(image, volumes=volumes, cleanup=True) as c:
        for output_line in c.run(do):
            print('{}:\t {}'.format(image, output_line))
