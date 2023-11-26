# mysql.vs.vertica
This is a repository for CS 511 - Advanced Data Management Project 4. In this repo. we include scripts used to benchmark MySQL and Vertica.

# MySql Container Configuration:
1. Start with a new fresh MySql Image: `sudo docker pull mysql`
2. Created a container named mysql-service with account:root password:root

   `docker run -d -p 3306:3306 --name mysql-service -e MYSQL_ROOT_PASSWORD=root  mysql`
4. Bash into the container just created. `docker exec -it mysql-service bash`
5. Located my.cnf location: `mysql --help | grep my.cnf`
6. In the OS that you're running the container, create a mount point for the container:
   
   `mkdir -p [your os mount point to store my.cof] && mkdir -p [your os mount point to store dataset]`

   for example: `mkdir -p /root/docker/mysql/conf && mkdir -p /root/docker/mysql/data`
7. Copied the my.cnf to OS directory mount point:

   `docker cp mysql-service:[your container mount point to store my.cof] [your os mount point to store my.cof]`

   for example: `docker cp mysql-service:/etc/mysql/my.cnf /root/docker/mysql/conf`
9. Delete the container, start a new one with proper mounting configuration. Please put your own mouting directory:

        sudo docker run --name mysql-server \
          -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root \
          --mount type=bind,src=/home/cs511/workplace/docker/mysql/conf/my.cnf,dst=/etc/mysql/my.cnf \ 
          --mount type=bind,src=/home/cs511/workplace/docker/mysql/data/tpch,dst=/etc/tpch \
          --mount type=bind,src=/home/cs511/workplace/docker/mysql/misc,dst=/etc/misc \
          --restart=on-failure:3 \
          -d mysql
# Common Docker commands to test MySQL Container:
  ### Manual invoke 1.sql query
  `sudo docker exec -i mysql-server mysql -uroot -proot tpch < /etc/tpch/queries/1.sql`

  ### Bash Into container
  `sudo docker exec -it mysql-server bash`

  ### Show Tables In TPCH database
  `sudo docker exec -it mysql-server mysql -uroot -proot -e "SHOW TABLES IN TPCH;"`

---

# Vertica Container Configuration:
1. Start with a new fresh Vertica Image: `sudo docker pull vertica/vertica-ce`
2. Created a container named vertica_container
   `sudo docker run -p 5433:5433 --name vertica_container -d vertica/vertica-ce`
3. Bash into the container just created. `docker exec -it vertica_container /bin/bash`
4. Make a new folder in the current directory using command in bash: `mkdir scripts`
5. Open a new terminal and execute the following command
   `chmod +x vertica_scripts/copy_file.sh`
   `sudo ./vertica_scripts/copy_file.sh`
   These command copy the scripts needed for setting up vertica database.
6. Go back to the original terminal with the container bash and execute the following command
   `chmod +x setup_vertica.sh`
   `./setup_vertica.sh`
   One thing to be careful is the node of the database may be different based on the machines. you can use `/opt/vertica/bin/admintools -t list_allnodes` to check the name of your node.
7. If you have used dbgen to create tbl files for data, you can now make tables in your vertica DB using the following command
   `chmod +x setup_tpch_schema.sh`
   `./setup_tpch_schema.sh`
Now you are all set to test TPCH queries using vertica DB, the time of execution for each query will be displayed in the end of each successful execution.

# Datas (Vertica)
https://docs.google.com/document/d/1IvXfwMJTjpJW4Nn_YcEuh4OTt7QMs_KpJncgJw2AAdw/edit?usp=sharing

# Datas (MySQL)
https://docs.google.com/document/d/1k4o7Kje2w7os2JuGqle4wDLOf6q5P5H7eEoulvujdHY/edit?usp=sharing
