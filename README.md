# yosacco
Yo SACCO is a web application written in Python to digitize credit communities. It has an admin portal to be used by the Yo office staffs to manage SACCOs and a frontend portal to be used by the SACCOs themselves.


Setting Up Databases
====================================================
Follow instructions below to set up the database.
1. Create the MySQL database on your system and obtain the credentials host,username,password and db 
2. cd into docs directory
3. import the database with the following command:
```
mysql {db_name} < schema.sql -u {db_user} -p
```
4. Now log into the database and check whether the database schema has been imported.

Configuration File
======================================================
1. Create a file called settings.cfg and place somewhere you can access it.
2. Set up an environment variable ADMINPORTAL_SETTINGS with value as path the above file. For example, run the following command
```
export ADMINPORTAL_SETTINGS=/path/to/settings.cfg 
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

