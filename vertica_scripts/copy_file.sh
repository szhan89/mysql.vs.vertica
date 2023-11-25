sudo docker cp vertica_scripts/setup_vertica.sh vertica_container:/home/dbadmin/scripts
sudo docker cp vertica_scripts/setup_tpch_schema.sh vertica_container:/home/dbadmin/scripts
sudo docker cp vertica_scripts/tbl_to_tpch.sql vertica_container:/home/dbadmin/scripts
sudo docker cp vertica_scripts/tpch_schema.sql vertica_container:/home/dbadmin/scripts
sudo docker cp vertica_scripts/run_queries.sh vertica_container:/home/dbadmin/scripts
sudo docker cp vertica_scripts/queries vertica_container:/home/dbadmin