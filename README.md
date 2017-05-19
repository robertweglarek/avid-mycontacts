# Requirements #
To run the project it's required to have `Docker` and `docker-compose` set up.
The rest will be handled by the application.


# Preparation #
To run the project you need to go to the `<project_root>/docker/` directory and
run:

* ` docker-compose up postgres` - give it few seconds to run and stop it (Ctrl+c). This is because some DB files need to be prepared first
* `docker-compose run --rm mycontacts python manage.py migrate` - this will build the image and migrate the database. It will close automatically and remove all intermediate containers
* `docker-compose run --rm mycontacts python manage.py createsuperuser` - will let you to create a superuser used to log in to admin panel for example. Will also clean all intermediate containers.

That's all, you're ready to go.


# Running the application #
To run the application, still in `/docker` dir, run: `docker-compose up`
This will run the database and django app (in `Debug` mode).

## Accessing the app ##
The application will run on: `http://localhost:8000`

Admin panel can be accessed on: `http://localhost:8000/admin/`

To log in and log out you can also use:
* `http://localhost:8000/api-auth/login/`
* `http://localhost:8000/api-auth/logout/`

## Browsable API ##
For an easier navigation, the browsable API is enabled. Project contains only
1 django app under: `http://localhost:8000/contacts/` - open it in the browser
to see available endpoints.

## bash access ##
The image also allows to access its `bash` console. Simply run:
`docker-compose run --rm mycontacts bash` and you'll be able to use container's
console.

# Testing #
To run tests simply run:
* `docker-compose up -d postgres` - this will run the database as a daemon. Avoids DB connection errors
* `docker-compose run --rm mycontacts python manage.py test --settings=mycontacts.settings.test`

You can also access the container's `bash` console and run tests dorectly from there:
* `docker-compose run --rm mycontacts bash`
* `./manage.py test --settings=mycontacts.settings.test`
