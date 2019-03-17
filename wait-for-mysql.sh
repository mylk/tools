#!/bin/bash
set -e

# change the parameters to your MySQL user, password and host (the value set with the -h parameter)
until mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} -hmysql -e "show databases;" &> /dev/null
do
    echo "Waiting for MySQL..."
    sleep 1
done

echo "MySQL is ready!"

