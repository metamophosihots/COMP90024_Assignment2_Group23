#!/bin/bash

. ./unimelb-comp90024-2021-grp-23-openrc.sh; ansible-playbook -i hosts all_in_one.yaml --ask-become-pass

# NmMwOWM4ODEyNGQ2MzM5











































docker create --name couchdb172.26.130.39 --env COUCHDB_USER=${user} --env COUCHDB_PASSWORD=${pass} --env COUCHDB_SECRET=${cookie} --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@172.26.130.39\"" --publish 5984:5984 --publish 4369:4369 --publish 9100-9200:9100-9200 ibmcom/couchdb3:${VERSION}
      

docker create\
      --name couchdb172.26.130.39\
      --env COUCHDB_USER=${user}\
      --env COUCHDB_PASSWORD=${pass}\
      --env COUCHDB_SECRET=${cookie}\
      --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@172.26.130.39\""\
      ibmcom/couchdb3:${VERSION}     
      
      
curl -XPOST "http://${user}:${pass}@172.26.128.24:5984/_cluster_setup" \
      --header "Content-Type: application/json"\
      --data "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\",\
             \"username\": \"${user}\", \"password\":\"${pass}\", \"port\": \"5984\",\
             \"remote_node\": \"172.26.133.245\", \"node_count\": \"4\",\
             \"remote_current_user\":\"${user}\", \"remote_current_password\":\"${pass}\"}"
             
curl -XPOST "http://admin:admin@172.26.128.24:5984/_cluster_setup"\
      --header "Content-Type: application/json"\
      --data "{\"action\": \"add_node\", \"host\":\"172.26.133.245\",\
             \"port\": \"5984\", \"username\": \"admin\", \"password\":\"admin\"}"

curl -XGET "http://${user}:${pass}@172.26.128.24:5984/"

curl -XPOST "http://${user}:${pass}@172.26.128.24:5984/_cluster_setup"\
    --header "Content-Type: application/json" --data "{\"action\": \"finish_cluster\"}"

curl -X GET "http://${user}:${pass}@172.26.130.39:5984/_membership"
             
curl -XPUT "http://${user}:${pass}@172.26.131.61:5984/twitter"

curl -X GET "http://${user}:${pass}@172.26.131.61:5984/_all_dbs"
curl -X GET "http://${user}:${pass}@172.26.130.39:5984/_all_dbs"
