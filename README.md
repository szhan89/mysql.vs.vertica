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
   
