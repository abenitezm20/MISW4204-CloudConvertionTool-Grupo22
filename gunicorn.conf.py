# Gunicorn configuration file 
# https://docs.gunicorn.org/en/stable/settings.html

# Workers
workers = 20
worker_class = 'gevent'

# Server socket
bind = '0.0.0.0:5000'

# The maximum number of pending connections.
backlog = 2048

# Debugging
debug = False
spew = False

# Logging
loglevel = 'info'
accesslog = '-'
errorlog = '-'
