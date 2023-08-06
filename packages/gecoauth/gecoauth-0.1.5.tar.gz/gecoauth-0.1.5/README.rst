=====
gecoauth
=====

gecoauth is a Django app that extends django-rest-auth, providing the same endpoints
but also adding some models and new functionality.
Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "gecoauth" to your INSTALLED_APPS setting like this::

    ``INSTALLED_APPS = [

        'gecoauth',
        'rest_framework',
        'rest_framework.authtoken', # token auth django rest
        'rest_auth', # django-rest-auth
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        'rest_auth.registration'
    ]``

2. Include the GecoAuth URLconf in your project urls.py like this::

    ``path('gecoauth/', include('gecoauth.urls'))``,

3. Add a site id ``SITE_ID = 1`` in settings

4. Add default authentication and permission classes 
    ``REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.TokenAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ]
    }``

5. Add the custom serializer
    ``REST_AUTH_REGISTER_SERIALIZERS = {
        'REGISTER_SERIALIZER': 'gecoauth.serializers.GecoRegisterSerializer',
    }``


6. Run ``python manage.py migrate`` to create the gecoauth models.

7. Start the development server and visit http://127.0.0.1:8000/gecoauth/rest-auth 
and http://127.0.0.1:8000/gecoauth/rest-auth-registration to use the app (see django-rest-auth
for the real endpoints)
