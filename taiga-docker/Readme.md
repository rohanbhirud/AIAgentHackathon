### Start the application

```bat
$ ./launch-taiga.bat
```

After some instants, when the application is started you can proceed to create the superuser with the following script:

```bat
$ ./taiga-manage.bat createsuperuser
```

The `taiga-manage.bat` script lets launch manage.py commands on the
back instance.
Use credentials:
- Username: admin
- Email: admin@example.com
- Password: adminpassword

You can access the application in **http://localhost:8080**.