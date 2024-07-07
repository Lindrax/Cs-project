# Cs-project
clone the repository 
go to /project
run python3 manage.py migrate
go to /server
run sqlite3 db.sqlite3 < db.sql
go back to ./project
run python3 manage.py runserver
