=====
gecoauth
=====

gecoauth is a Django app that extends django-rest-auth, providing the same endpoints
but also adding some models and new functionality.
Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "gecoauth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'gecoauth',
    ]

2. Include the GecoAuth URLconf in your project urls.py like this::

    path('gecoauth/', include('gecoauth.urls')),

3. Run ``python manage.py migrate`` to create the gecoauth models.

4. Start the development server and visit http://127.0.0.1:8000/gecoauth/rest-auth 
and http://127.0.0.1:8000/gecoauth/rest-auth-registration to use the app (see django-rest-auth
for the real endpoints)
