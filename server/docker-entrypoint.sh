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
    exec celery -A osat worker -l info $@
  ;;

  'beat')
    shift
    exec celery -A osat beat -l info $@
  ;;

  'migrate')
    shift
    exec python3 manage.py migrate $@
  ;;

  'createsuperuser')
   	shift
   	exec python3 manage.py createsuperuser $@
  ;;

  'bash')
  	ARGS=""
  	shift
    apk add --update --no-cache nano bash jq 
  	exec /bin/bash $@
	;;

  *)
    python3 manage.py migrate
  	exec python3 manage.py runserver $@
	;;
esac
