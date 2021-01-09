#!/bin/sh

set -x
set -e

isArgPassed() {
  arg="$1"
  argWithEqualSign="$1="
  shift
  while [ $# -gt 0 ]; do
    passedArg="$1"
    shift
    case $passedArg in
    $arg)
      return 0
      ;;
    $argWithEqualSign*)
      return 0
      ;;
    esac
  done
  return 1
}

case "$1" in

  'worker')
    shift
    exec celery -A core worker -l info
  ;;

  'beat')
    shift
    exec celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
  ;;

  'migrate')
    shift
    exec python3 manage.py migrate
  ;;

  'makemigrations')
    shift
    exec python3 manage.py makemigrations
  ;;

  'createsuperuser')
   	shift
   	exec python3 manage.py createsuperuser
  ;;

  'django')
   	shift
    python3 manage.py migrate
   	exec python manage.py runserver 0.0.0.0:8000
  ;;

  'bash')
  	ARGS=""
  	shift
    # apk add --update --no-cache nano bash jq 
  	exec /bin/bash $@
	;;

  *)
    
  	exec echo $@
	;;
esac
