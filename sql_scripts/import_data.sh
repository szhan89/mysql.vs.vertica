#!/bin/bash
sudo docker exec mysql-server mkdir -p /etc/tpch
sudo docker exec mysql-server mkdir -p /etc/tpch/queries

for file in /home/cs511/workplace/TPCH/dbgen/*.tbl; do
    sudo docker cp "$file" mysql-server:/etc/tpch/
done

for query in /home/cs511/workplace/queries-tpch-dbgen-mysql/*.sql; do
    sudo docker cp "$query" mysql-server:/etc/tpch/queries
done
