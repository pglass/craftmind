SHELL := /bin/bash

start: stop
	gunicorn --access-logfile - --error-logfile - -w 2 -b 0.0.0.0:52425 craftmind.app:app

stop:
	-pkill -f 'gunicorn.*craftmind'
