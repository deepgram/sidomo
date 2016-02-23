from sdpm import Container


def hello(to):
    """Just say it."""
    with Container(
        'ubuntu',
        memory_limit_gb=2,
        stderr=False
    ) as c:
        for line in c.run(
            'bash -c \"\
                echo hello %s\
            \"\
            ' % to
        ):
            yield line


if __name__ == '__main__':
    for line in hello("world"):
        print line
