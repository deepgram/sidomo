# sdpm

###Simple Docker Python Module

####Manages the lifecycle of a docker container.

If you can get your software to work in a docker container, then this module will make it work in Python.


####How to install:
```bash
pip install -e git+https://github.com/noajshu/sdpm.git#egg=sdpm
```

####How to use:
```python
from sdpm import Container

with Container('ubuntu') as c:
    for output_line in c.run('bash -c "echo hello world"'):
        print(output_line)
```