# sdpm
Simple Docker Python Module

Manages the lifecycle of a docker container.

Your software...
- Breaks on Java verions after 1.7?
- Only works on Ubuntu 6.06 (Dapper Drake)?
- Depends on MS Word macros?

If you can get it to work in docker container,
then this module will make it work in python.

Ex:

from sdpm import Container

with Container('ubuntu') as c:
    for output_line in c.run('bash -c "echo hello world"'):
        print(output_line)
