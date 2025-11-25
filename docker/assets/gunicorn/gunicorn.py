from monitoring.metrics import mark_process_dead

bind = '0.0.0.0:8000'
workers = 2
timeout = 120
name = 'app'
errorlog = '-'
loglevel = 'debug'
accesslog = '-'
access_log_format = '%(t)s "%(r)s" %(l)s %(q)s %(s)s "%(f)s" %({X-Request-Id}i)s %(u)s "%(a)s"'


def child_exit(server, worker):
    mark_process_dead(worker)
