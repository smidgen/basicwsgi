# basicwsgi
A basic, framework-less Python WSGI web application, with sample Environment dump and MySQL access pages. This is meant as a base for future projects.

This is a Python 3 app.

## Setup
Setup instructions for Apache.

1. Install Apache, WSGI, and Python-MySQLdb. The following command works for distros using Ubuntu repositories.

        sudo apt-get install apache2 libapache2-mod-wsgi-py3 python3-mysqldb

2. Check out the repository to your chosen location on your server. In these instructions, we'll put it in <code>/srv/basicwsgi/</code>

3. Edit the Apache vhost configuration file, for example, <code>/etc/apache2/sites-enabled/000-default.conf</code> or <code>/etc/apache2/sites-enabled/default-ssl.conf</code>. Add the following lines:

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

4. On a developement server, you may wish to change the loglevel to <code>info</code> in order to get more detailed information (such as WSGI process restarts) in <code>/var/log/apache2/error.log</code>.

5. Set up a MySQL user and database, grant privileges for that database, create the test table, and insert some data. The simplest way to go about this is to update the password in <code>install/dbsetup.sql</code> and run it.

6. Browse to [http://localhost/basicwsgi/](http://localhost/basicwsgi/), or whatever your url is based on your configuration.
