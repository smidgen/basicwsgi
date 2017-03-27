# basicwsgi
A basic, framework-less Python WSGI web application, with sample Environment dump and MySQL access pages. This is meant as a base for future projects.

This is a Python 3 app.

## Setup
How to get Python3 + WSGI + Apache HTTPD running on Linux.

### Ubuntu-based distros
The following instructions should work for any Ubuntu-based Linux distro. It has been tested on Linux Mint.

1. Install Apache, WSGI, and Python-MySQLdb. The following command works for distros using Ubuntu repositories.

        sudo apt-get install apache2 libapache2-mod-wsgi-py3 python3-mysqldb

2. Check out the repository to your chosen location on your server. In these instructions, we'll put it in <code>/srv/basicwsgi/</code>

3. Edit the Apache vhost configuration file, for example, <code>/etc/apache2/sites-enabled/000-default.conf</code> or <code>/etc/apache2/sites-enabled/default-ssl.conf</code>. Add the following lines:

```ApacheConf
        WSGIDaemonProcess basicwsgi processes=2 threads=5
        WSGIProcessGroup basicwsgi

        WSGIScriptAlias /basicwsgi /srv/basicwsgi/application.wsgi

        <Directory /srv/basicwsgi>
                Options None
                AllowOverride None
                Require all granted
        </Directory>

        Alias "/basicwsgi/assets/" /srv/basicwsgi/assets/
        <Directory /srv/basicwsgi/assets>
                Options None
                AllowOverride None
                Require all granted
        </Directory>
```

4. On a developement server, you may wish to change the loglevel to <code>info</code> in order to get more detailed information (such as WSGI process restarts) in <code>/var/log/apache2/error.log</code>.

5. Set up a MySQL user and database, grant privileges for that database, create the test table, and insert some data. The simplest way to go about this is to update the password in <code>install/dbsetup.sql</code> and run it.

6. Update the MySQL configuration in <code>config.py</code>.

7. Update the paths and base URL in <code>application.wsgi</code>.

8. Open the appropriate firewall port (usually TCP port 80) if necessary.

9. Browse to [http://localhost/basicwsgi/](http://localhost/basicwsgi/), or whatever your url is based on your configuration.

### CentOS
The following instructions have been tested on CentOS 7, starting with the minimal ISO install.

1. Some extremely useful tools that every command-line guru knows (substitute nano with your favorite text editor):

        sudo yum install nano net-tools screen

2. Dependencies for code compilation:

        sudo yum -y groupinstall development
2. Add repo:

        sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
3. Search for the latest available version of Python to use in the next command:

        sudo yum search python3
4. Install mod_wsgi and its dependencies, including Python3 and Apache
    (be sure to use the above yum search command to check if
    python36u-mod_wsgi is still the latest version)

        sudo yum -y install python36u-mod_wsgi

5. To start Apache without rebooting the server

        sudo systemctl enable httpd
        sudo systemctl start httpd

6. To open the firewall port (very important!)

        sudo firewall-cmd --zone=public --add-port=80/tcp --permanent
        sudo firewall-cmd --reload

7. So you can use /usr/bin/python3 in the shebang line

        sudo ln -s /usr/bin/python3.6 /usr/bin/python3

8. Install Python3 MySQLdb driver.
    Again, do a yum search to get the latest available version of Python3.

        sudo yum -y install python36u-pip python36u-devel
        sudo yum -y install mariadb mariadb-server mariadb-devel
        sudo pip3.6 install mysqlclient
9. Start MariaDB/MySQL.

        sudo systemctl enable mariadb
        sudo systemctl start mariadb
10. Check out the project (modify the path and username in the following commands to suit).

        cd /srv
        sudo mkdir basicwsgi && sudo chown nolan:nolan basicwsgi
        git clone https://github.com/smidgen/basicwsgi.git basicwsgi

11. Edit <code>application.wsgi</code> and update the appropriate paths and URL. Be sure to change it from localhost to whatever hostname you're using.

        sudo nano application.wsgi

12. Create a Apache configuration file in <code>/etc/httpd/conf.d/</code>.

        sudo nano /etc/httpd/conf.d/basicwsgi.conf
    Fill it with the following:

```ApacheConf
        WSGIDaemonProcess basicwsgi processes=2 threads=5
        WSGIProcessGroup basicwsgi

        WSGIScriptAlias /basicwsgi /srv/basicwsgi/application.wsgi

        <Directory /srv/basicwsgi>
                Options None
                AllowOverride None
                Require all granted
        </Directory>

        Alias "/basicwsgi/assets/" /srv/basicwsgi/assets/
        <Directory /srv/basicwsgi/assets>
                Options None
                AllowOverride None
                Require all granted
        </Directory>
```

13. On a developement server, you may wish to change the loglevel in <code>/etc/httpd/conf/httpd.conf</code> to <code>info</code> in order to get more detailed information (such as WSGI process restarts) in <code>/etc/httpd/logs/error_log</code>

14. Reload Apache configuration files to get it going:

        sudo systemctl reload httpd
15. Get SELinux to stop raining on your parade:

        chcon -R -t httpd_sys_content_t /srv/basicwsgi
16. Set up a MySQL user and database, grant privileges for that database, create the test table, and insert some data. The simplest way to go about this is to update the password in install/dbsetup.sql and run it.

        sudo nano /srv/basicwsgi/install/dbsetup.sql
        mysql -uroot

    Then in the MariaDB command line:

        source /srv/basicwsgi/install/dbsetup.sql
        quit;
17. Change the MySQL password in <code>/srv/basicwsgi/config.py</code>.

        sudo nano /srv/basicwsgi/config.py
18. Browse to [http://localhost/basicwsgi/](http://localhost/basicwsgi/), or whatever your url is based on your configuration.

## Development Tips
* Remember that whenever you make a code change to the WSGI application, you'll need to update the last modified date on <code>application.wsgi</code>.

        touch /srv/basicwsgi/application.wsgi
* During development, you pretty much have to keep a terminal window open with <code>tail -f</code> monitoring the Apache error log in order to see parse errors and things that can cause the error system to fail.

    For Debian/Ubuntu-based systems:

        sudo tail -f /var/log/apache2/error.log
    For CentOS:

        sudo tail -f /etc/httpd/logs/error_log
    * Due to this, if you have a server on which multiple WSGI applications are running, it may be wise to create a separate Apache log file for each one, so you don't have error messages from all the applications mixed together.

#### Resources
The installation instructions for Python3 on CentOS were modified from the following article, which also explains some of the how's and why's, takes you through creating a virtualenv, and helps you create a basic Python (not WSGI) hello world.
[https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-centos-7](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-centos-7)
