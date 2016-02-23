from sidomo import Container


def say_hello(to):
    """Just say it."""
    with Container(
        'ubuntu',
        stderr=False
    ) as c:
        for line in c.run(
            'echo hello %s' % to
        ):
            yield line


if __name__ == '__main__':
    for line in say_hello("world"):
        print line
