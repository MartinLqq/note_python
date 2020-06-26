# !/bin/bash
:<<!
        Shell Tests
!
# This is a single line quote


# Print
# echo 'Hello shell'


# Define a local variable
name=Martin
# name='Leo'
# name="John $SHELL"
# name=`pwd`
# name=$(pwd)


# Use global variables
# env  # Show all globals
# echo $SHELL
# env | grep SHELL


# Define a global variable
# export TEST_SHELL=123
# TEST_SHELL=123
# export TEST_SHELL
# echo $TEST_SHELL


# Get the value of a variable
# echo $name
# echo "$name"
# echo ${name}
# echo "${name}"   # standard


# Unset a variable
# unset name
# echo "${name}"


# Builtin variables

# Get the filename of current script
# echo "${0}" ---  $0 --- "$0" --- ${0}

# Get the params of current script: "${n}"
# echo "${1}" -- "${2}" -- "${3}"
# echo $0 -- $1 -- $2 -- $9 -- ${10}

# Get total params
# echo "The total params is $#"


# String slice
str="abcdefg1234567"
# echo "The origin string is $str.   The sub string is  ${str:0:5}"
# echo "The origin string is $str.   The sub string is  ${str:0-5:3}"


# Default value
# echo "${aaa:-100}"   # output: 100
# aaa=90
# echo "${aaa:-100}"   # output: 90
# echo "${aaa:+100}"   # output: 100



# Conditional expression

# logical exp: && ||
# [ 1 = 1 ] && echo "Success"
# test 1 = 1 && echo "Success"
# [ 1 = 2 ] || echo "Fail"

# file exp: -f -d -x
# [ -f test.sh ] && echo "Is a file"
# [ -f test.xx ] || echo "Is not a file"
# [ -d test.sh ] || echo "Is not a directory"
# [ -x test.sh ] && echo "Can be executed"

# number operations: = -eq -gt -lt -ne
[ 1 -eq 1 ] && echo "1 equal to 1"

# string compare
[ '123' == '123' ] && echo 'Equal'
[ '123' == '456' ] || echo 'Not equal'

# test by echo $?
# [ 1 = 1 ]
# echo $?

# calculate exp: $(( calculation ))
# echo $(( 2*5 ))   # only support +-*/ and can only calculate integer.
# a=2
# echo $((a*5))
# let ret=3*5
# echo $ret



# Useful simbol

# redirect:  >  >>

# pipe:  |

# to backend:  &

# msg symbol:  1>>  2>>  2>&1
# bash test.sh 1>> ok.log 2>> err.log
# bash test.sh >> all.log 2>&1



# Linux wastebin
# /dev/null

