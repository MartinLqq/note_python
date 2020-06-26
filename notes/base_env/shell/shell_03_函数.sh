# !/bin/bash


echo '-------1--------'
say(){
    echo 'Hello shell!'
}
say


echo '-------2--------'
say(){
    echo "Hello $1 $2 $3!"
}
say Martin John


echo '-------3--------'
say(){
    echo "Hello $1"
    echo "Hello ${1:-Martin}"
}
say $1


echo '-------4--------'
#!/bin/bash

arg="$1"

usage(){
  echo "The usage of $0:  $0 [ start|stop|restart ]"
}

if [ $# -eq 1 ]
then
  case "${arg}" in
    start)
      echo "Server is starting..."
      ;;
    stop)
      echo "Server is stoping..."
      ;;
    restart)
      echo "Server is restarting..."
      ;;
    *)
      usage
    ;;
  esac
else
  usage
fi




