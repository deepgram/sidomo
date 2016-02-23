#Sidomo

##Simple Docker Module

###If you can get your software to work in a docker container, then this module will make it work in Python.

####How to install:
```bash
pip install -e git+https://github.com/noajshu/sidomo.git#egg=sdpm
```

####How to use:
```python
from sidomo import Container

with Container('ubuntu') as c:
    for output_line in c.run('echo hello world'):
        print(output_line)
```

####Examples:
- hello_world.py is 'Hello, World!' as a module
- ffmpeg.py fetches audio from a URL and transcodes it to WAV format

####Ideas:
- Replace leaky glue code
- Run Erlang from Python
- Resurrect legacy software for use in a modern environment
- Make a Python module more portable (the only dependency is Docker itself)
