# !/bin/bash

:<<!
        Tests for flow control
!


echo '---------------if-----------------'

if [ "${1}" = 'Martin' ]
then 
    echo 'Hello, Martin'
elif [ "$1" = 'John' ]
then
    echo 'Hi, John'
else
    echo 'Bye, stranger!'
fi



echo '-------------case-------------------'

case "$1" in
   'Martin')
        echo 'Hello Martin'
        ;;
    'John')
        echo 'Hello John'
        ;;
esac



echo '--------------for------------------'

for i in $( ls /tmp)
do
    echo "${i}"
done


echo '---------------while-----------------'

a=1
while [ "${a}" -lt 5 ]
do
    echo "${a}"
    a=$((a+1))
done





echo '---------------until-----------------'

b=1
until [ "${b}" -eq 8 ]
do
    echo "${b}"
    b=$((b+1))
done

