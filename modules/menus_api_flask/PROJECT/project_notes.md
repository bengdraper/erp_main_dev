** init db schema @ ./menu_db_init.sql
// i.e. run ...init.sql through docker to inst db from file
cat menu_db_init.sql | docker exec -i pg_container psql -d menus_project

*** backup
$ docker cp pg_container:menus_dump.sql data
$ docker exec pg_container pg_dump --verbose --file menus_dump.sql menus_project

$ docker exec pg_container psql -c 'CREATE DATABASE menus_project_new;'

// slurp dump file into new db
$ docker exec pg_container psql menus_project_new -f menus_dump.sql