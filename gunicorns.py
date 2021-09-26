# errorlog = './logs/gunicorn.error.log'
loglevel = 'debug'
keepalive = 5
# accesslog = './logs/gunicorn.access.log'
bind = '0.0.0.0:5001'
backlog = 2048
# workers = 1

threads = 2
worker_class = 'gevent'
