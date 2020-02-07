#!/bin/bash

backup_home=/home/nobody/backup
cd $backup_home
exec >backup2.log 2>&1

kinit svc@DOMAIN.RU -k -t $backup_home/svc.keytab

db="database"
user="backadm"
export PGPASSWORD=$(cat $backup_home/.hidden2.lck | openssl enc -base64 -d -aes-256-cbc -nosalt -pass pass:********************)
dbhost="10.10.106.59"
dbport="30402"
file="$(date +%Y-%m-%d_%H-%M).gz"
masters=("http://master2.domain.ru:14000/webhdfs/v1/user/svc/backup/postgres/" "http://master.domain.ru:14000/webhdfs/v1/user/svc/backup/postgres/")
op="?op=LISTSTATUS"
op_write="?op=CREATE&data=true"
cmd="curl -s -o /dev/null --negotiate -u : -w %{http_code}"
cmd_write="curl --header "Content-Type:application/octet-stream" -XPUT --data-binary @- --negotiate -u : -i -s -o /dev/null -w %{http_code}"
timeout="-m 100"

for master in "${masters[@]}"; do

out=$($cmd $timeout $master$op)

if [ $out -ne 200 ]; then
    echo "Curl connection failed with return code: $out"
else
    if [ $out -eq 200 ]; then
        echo "Curl check webhdfs operation return code: $out"
        echo "Running backup..."
        /usr/pgsql-9.6/bin/pg_dump -U$user -h $dbhost -p $dbport -Z -F=t $db | out=$($cmd_write $timeout $master$file$op_write)
        echo "Archive path $master$file?op=OPEN"
        echo "Curl write webhdfs operation return code: $out"
        cat backup2.log | mailx -s "Postgres Database Backup" -S smtp=smtp://mailinternal.domain.ru -S from="Postgres Database Backup <svc@domain.com>" alexey.shcherbakov@domain.com
        exit;
    fi
fi
done;

###################################################################################################################
#####
##### Setup extended acl
#####
##### hdfs dfs -setfacl -R -m user:svc:rwx,group:sentry-admins:rwx,other::--- /user/svc
##### hdfs dfs -setfacl -m default:group:sentry-admins:rwx,other::--- /user/svc
#####
##### Reset acl
#####
##### hdfs dfs -setfacl -x default:group:sentry-admins /user/svc
##### hdfs dfs -setfacl -R -x user:svc,group:sentry-admins /user/svc
#####
###################################################################################################################


#########
######### echo '*********************' | openssl enc -base64 -e -aes-256-cbc -nosalt  -pass pass:***************** > .hidden2.lck
#########
