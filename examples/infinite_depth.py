"""Never tested. Open up containers within containers forever."""
import os
from sidomo import Container


level = 0

with open(os.path.abspath(__file__), "r") as infile:
    self_str = "".join(infile.readlines).replace(
        "level = %s" % level,
        "level = %s" % (level + 1)
    )

print "Hello from level %s" % level

with Container('docker_and_sidomo_img') as c:
    for line in c.run(
        'bash -c "echo ' + self_str + ' > infinite_depth.py;' +
        'python infinite_depth.py;"'
    ):
        print line
