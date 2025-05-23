# yosacco
Yo SACCO is a web application written in Python to digitize credit communities. It has an admin portal to be used by the Yo office staffs to manage SACCOs and a frontend portal to be used by the SACCOs themselves.


Setting Up Databases
====================================================
Follow instructions below to set up the database.
1. Create the MySQL database on your system and obtain the credentials host,username,password and db.
Use the following commands to create the database and the use:
```
mysql -u root -p
create database yosacco;
create user yosacco@localhost identified by "************";
grant all privileges on yosacco.* to "yosacco"@"localhost";
```

#To see the databases, run the following command
```
show databases;
```
```
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| yosacco            |
+--------------------+
5 rows in set (0.01 sec)
```

# To use/open a database, use the following command:
```
use yosacco;
```

#To list tables in our yosacco database, use the following command:
```
show tables;
```

```
+-------------------+
| Tables_in_yosacco |
+-------------------+
| acg               |
| audit_trail       |
| sacco             |
| sacco_member      |
| transaction_log   |
| user              |
| user_acg          |
+-------------------+
7 rows in set (0.01 sec)
```

# To import the database, run the following command:
```
cd docs
mysql yosacco < schema.sql -u yosacco -p
```
# To import changes, run the following command:
```
mysql yosacco < db_changes/20240716_jt.sql -u yosacco -p
```
2. cd into docs directory
3. import the database with the following command:
```
mysql {db_name} < schema.sql -u {db_user} -p
```
4. Now log into the database and check whether the database schema has been imported.

Configuration File
======================================================
1. Create a file called settings.cfg and place it somewhere you can access it.
2. Add the following configs to the settings.cfg file.
```
SECRET_KEY = '****YOUR SECRET KEY*****'

# MySQL Settings
MYSQL_HOST = '****YOUR HOST*****'
MYSQL_USER = '****YOUR DB USERNAME*****'
MYSQL_PASSWORD = '****YOUR DB PASSWORD*****'
MYSQL_DB = '****YOUR DB NAME*****'

#supported languages
LANGUAGES = ['en', 'es']
```
Note: Use the following guide to generate a secure secret key:
How to generate good secret keys
A secret key should be as random as possible. Your operating system has ways to generate pretty random data based on a cryptographic random generator. Use the following command to quickly generate a value for Flask.secret_key (or SECRET_KEY):
```
$ python -c 'import secrets; print(secrets.token_hex())'
'192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
```

3. Set up an environment variable ADMINPORTAL_SETTINGS with value as path to the above file. For example, run the following command
```
export ADMINPORTAL_SETTINGS=/home/rodney/projects/yosacco/adminportal 
OR
set 
```
Ensure that you set the right path.


Setting up Initial Admin User
======================================================
1. cd into adminportal/cli/
2. run the command:
```
flask create-user
```
3. Provide the name, email, phone and password.
4. The user shall be created. If the user already exists, they will be updated with the new data given

Creating python Virtual Environments (env)
======================================================
```
python -m venv yosacco-env
source  yosacco-env/bin/activate

```
To Deactivate, run the following command
```
deactivate
```

Issue installing flask_mysqldb/mysqlclient
=======================================================
Run the following command
yum install python3-devel mysql-devel pkgconfig

Running your Flask Application
=======================================================
From the root directory, run the following command:
flask --app adminportal run --debug