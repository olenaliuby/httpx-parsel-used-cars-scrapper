#!/bin/bash
# Script to create a database dump and save it in the "dumps" folder

backup_time="$BACKUP_TIME"

current_datetime=$(date +'%Y-%m-%d_%H-%M')

dump_filename="backup_${current_datetime}.sql"

backup_directory="dumps"

mkdir -p "$backup_directory"

export POSTGRES_USER=postgres
export POSTGRES_DB=app

current_time=$(date +'%H:%M')
if [ "$current_time" == "$backup_time" ]; then
    pg_dump -U "DB_USERNAME" -d "DB_DATABASE" > "$backup_directory/$dump_filename"

    echo "The database has been successfully backed up to: $backup_directory/$dump_filename"
else
    echo "Database backup is not scheduled at the current time: $current_time"
fi
