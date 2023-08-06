#!/bin/bash

DATABASE=./todo.db

if [[ -e $DATABASE ]]; then
    python todos.py purge users
    python todos.py purge todos
fi

python todos.py create user Tom   -e tom@email.com -p 212-555-1234
python todos.py create user Dick  -e dick@email.com
python todos.py create user Harry -p 212-123-5555

python todos.py create todo Tom title1 -c description1 -d 2020-11-30
python todos.py create todo Tom title2 -c description2 --due-date=2020-12-31
python todos.py create todo Harry todo-1 --description=Christmas-party -d 2020-11-30
python todos.py create todo Harry todo-2 --description=New-Year-party

python todos.py update user email Harry harry@email.com
python todos.py update user phone Dick 203-555-1212

python todos.py update todo title 4 most-important
python todos.py update todo description 4 2021-party

python todos.py show users
python todos.py show todos

echo "running SQL on $DATABASE:"
echo "-------------------------"
echo
query="select * from User;"
echo "$query"
sqlite3 todo.db "$query"
echo 
query="select * from Todo;"
echo "$query"
sqlite3 todo.db "$query"
echo
