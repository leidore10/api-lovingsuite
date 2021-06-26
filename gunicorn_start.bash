#!/bin/bash

NAME="sandbox"                                  # Name of the application
DJANGODIR=/home/pose/projects/sandbox-backend             # Django project directory
SOCKFILE=/home/pose/projects/sandbox-backend/run/gunicorn.sock  # we will communicte using this unix socket
USER=www-data                                        # the user to run as
GROUP=www-data                                     # the group to run as
NUM_WORKERS=1                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=conf.settings.prod             # which settings file should Django use
DJANGO_WSGI_MODULE=sandbox.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/pose/.virtualenvs/sandbox-backend/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)

NUM_WORKERS=3
TIMEOUT=600

exec /home/pose/.virtualenvs/sandbox-backend/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-