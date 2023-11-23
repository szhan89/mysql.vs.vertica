COPY tpch.nation FROM '/home/dbadmin/dbgen/nation.tbl' DELIMITER '|' DIRECT;
COPY tpch.region FROM '/home/dbadmin/dbgen/region.tbl' DELIMITER '|' DIRECT;
COPY tpch.part FROM '/home/dbadmin/dbgen/part.tbl' DELIMITER '|' DIRECT;
COPY tpch.supplier FROM '/home/dbadmin/dbgen/supplier.tbl' DELIMITER '|' DIRECT;
COPY tpch.partsupp FROM '/home/dbadmin/dbgen/partsupp.tbl' DELIMITER '|' DIRECT;
COPY tpch.customer FROM '/home/dbadmin/dbgen/customer.tbl' DELIMITER '|' DIRECT;
COPY tpch.orders FROM '/home/dbadmin/dbgen/orders.tbl' DELIMITER '|' DIRECT;
COPY tpch.lineitem FROM '/home/dbadmin/dbgen/lineitem.tbl' DELIMITER '|' DIRECT;

