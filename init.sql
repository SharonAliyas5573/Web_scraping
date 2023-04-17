CREATE USER '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'%';

CREATE DATABASE ${MYSQL_DATABASE};

USE ${MYSQL_DATABASE};

CREATE TABLE urls (
    
    url VARCHAR(255) NOT NULL,
   
);

CREATE TABLE news (
    
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    image_url VARCHAR(255),
   
);
