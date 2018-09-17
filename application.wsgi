activate_this = '/home/ubuntu/juleslasne/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stdout)
sys.path.insert(0, "/var/www/html/juleslasne/")

from website import application
