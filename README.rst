==============
DRF Compose
==============

.. image:: https://img.shields.io/pypi/v/drf_compose.svg
        :target: https://pypi.python.org/pypi/drf_compose

.. image:: https://img.shields.io/travis/IamAbbey/drf_compose.svg
        :target: https://travis-ci.com/IamAbbey/drf_compose

.. image:: https://readthedocs.org/projects/drf-compose/badge/?version=latest
        :target: https://drf-compose.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/IamAbbey/drf_compose/shield.svg
     :target: https://pyup.io/repos/github/IamAbbey/drf_compose/
     :alt: Updates

DRF Compose is a Python package for defining and quick starting Django
Rest Framework projects. With DRF Compose, you use a JSON or YAML file
to configure your DRF application. Then, with a single command, you get
to generate your DRF project code using all the specified configuration
from your compose file. To learn more about all the features of DRF
Compose, see the list of features below.

DRF Compose is aimed at making the process of starting a DRF project
quick and fun - giving you a development head start experience - while also preventing 
any frustration caused by the inability to quick start an API.

Installing
==========

Install and update using
`pip <https://pip.pypa.io/en/stable/getting-started/>`__:

.. code-block:: bash

   $ pip install drf-compose

Usage
=====

Using DRF Compose is basically a two-step process:

-  Define your application in a drf-compose.json file.
-  Run drf-compose and the DRF compose command generates a ready to use
   DRF project code.

Command options overview and help
=================================
You can also see this information by running drf-compose --help from the command line.

.. code-block:: bash

    Usage: drf-compose [OPTIONS]

      This script composes a DRF project.

    Options:
      -s, --source FILE  Specify an alternate compose file as source  [default: drf-compose.json]
      --yaml             Indicates that the supplied source file is a YAML file
      --help             Show this message and exit.

A drf-compose file looks like this:

.. raw:: html

   <table style="width:100%;">

.. raw:: html

   <tr>

.. raw:: html

   <td>

In YAML format (.yml)

.. raw:: html

   </td>

.. raw:: html

   <td>

In JSON format (.json)

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td>

.. code-block:: yaml

    name: delight_blog
    app_with_model:
    - app_name: post
      models:
      - name: Post
        fields:
        - name: title
          type: char
          options:
            max_length: 200
        - name: content
          type: text
          options:
            blank: true
            'null': true
        str: title
      - name: Category
        fields:
        - name: name
          type: char
          options:
            blank: true
            'null': true
            max_length: 200

.. raw:: html

   </td>

.. raw:: html

   <td>

.. code-block:: javascript

   {
     "name": "delight_blog",
     "app_with_model": [
       {
         "app_name": "post",
         "models": [
           {
             "name": "Post",
             "fields": [
                {
                  "name": "title",
                  "type": "char",
                  "options": {
                    "max_length": 200
                  }
                },
               {
                 "name": "content",
                 "type": "text",
                 "options": {
                    "blank": true,
                    "null": true
                  }
               }
             ],
             "str": "title"
           },
           {
             "name": "Category",
             "fields": [
               {
                 "name": "name",
                 "type": "char",
                 "options": {
                    "blank": true,
                    "null": true,
                    "max_length": 200
                  }
               }
             ]
           }
         ]
       }
     ]
   }

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   </table>


Options
=======

1. ``name`` *(required)*: specifies the project name.
2. ``app_with_model`` *(required)*: specifies details describing each apps
   in the DRF project.

   -  ``app_name`` *(required)*: specifies the app name 
   -  ``models``: a list of models belonging to the app

      -  ``name`` *(required)*: specifies the model name 
      -  ``meta``: specifies the different model meta options as in the
         `Django model meta
         documentation <https://docs.djangoproject.com/en/3.2/topics/db/models/#meta-options>`__
      -  ``fields`` *(required)*: a list of fields belonging to a model.

         -  ``name`` *(required)*: the name of the field as in the
            `Django model field documentation
            <https://docs.djangoproject.com/en/3.2/topics/db/models/#fields>`__
         -  ``type`` *(required)*: the field type as specified in
            `Django model field type reference
            documentation <https://docs.djangoproject.com/en/3.2/ref/models/fields/#model-field-types>`__.
            Basic syntax sugar also supported as shown below:
            
            ================  ============================================================
            Syntax            Field Type
            ================  ============================================================
            char              CharField
            text              TextField
            url               URLField
            datetime          DatetimeField
            fk                ForeignKey
            o2o               OneToOneField
            m2m               ManyToManyField
            ================  ============================================================
            
         -  ``options``: specifies field option as in the `Django model
            field
            documentation <https://docs.djangoproject.com/en/3.2/ref/models/fields/>`__.

      -  ``use_uuid_as_key`` *(boolean)*: if True, a UUID is used as the
         model’s primary key.
      -  ``str``: specifies the field to be returned as representation
         of the model in ``__str__``. **Must be one of the specified
         field names**
3. ``auth_app``: specifies details of the authentication application.

   -  ``app_name`` *(required)*: specifies the app name
   -  ``model_name`` *(required)*: specifies the model name for the custom user model
   -  ``username_field``: A string describing the name of the field on the user model that is used as the unique identifier `Django USERNAME_FIELD documentation            <https://docs.djangoproject.com/en/3.2/topics/auth/customizing/>`__.
   -  ``email_field``: A string describing the name of the email field on the User model.
      `Django's EMAIL_FIELD documentation <https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#django.contrib.auth.models.CustomUser.EMAIL_FIELD>`__
   -  ``required_fields``: A list of the field names that will be prompted for when creating a user via the ``createsuperuser`` management command
      `Django's REQUIRED_FIELDS documentation <https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#django.contrib.auth.models.CustomUser.REQUIRED_FIELDS>`__
   -  ``meta``: specifies the different model meta options as in the
      `Django model meta
      documentation <https://docs.djangoproject.com/en/3.2/topics/db/models/#meta-options>`__
   -  ``fields``: a list of fields belonging to a model.

      -  ``name`` *(required)*: the name of the field as in the
         `Django model field documentation
         <https://docs.djangoproject.com/en/3.2/topics/db/models/#fields>`__
      -  ``type`` *(required)*: the field type as specified in
         `Django model field type reference
         documentation <https://docs.djangoproject.com/en/3.2/ref/models/fields/#model-field-types>`__.
         Basic syntax sugar also supported as shown below:
         
         ================  ============================================================
         Syntax            Field Type
         ================  ============================================================
         char              CharField
         text              TextField
         url               URLField
         datetime          DatetimeField
         fk                ForeignKey
         o2o               OneToOneField
         m2m               ManyToManyField
         ================  ============================================================
         
      -  ``options``: specifies field option as in the `Django model
         field
         documentation <https://docs.djangoproject.com/en/3.2/ref/models/fields/>`__.

   -  ``use_uuid_as_key`` *(boolean)*: if True, a UUID is used as the
      model’s primary key.
   -  ``str``: specifies the field to be returned as representation
      of the model in ``__str__``. **Must be one of the specified
      field names**
4. ``include``: specifies the addons to be included in the application.

   -  ``simple_jwt`` *(boolean)*: if True, includes `Simple JWT <https://github.com/jazzband/djangorestframework-simplejwt>`__ JSON Web Token authentication plugin into the application.
   
      **COMING SOON!**
   -  ``django_filter`` *(boolean)* if True, includes `Django-filter <https://github.com/carltongibson/django-filter>`__, a reusable Django application allowing users to declaratively add dynamic QuerySet filtering from URL parameters.
   -  ``docker`` *(boolean)*: if True, includes docker setup option into the application.
   -  ``dj-database-url`` *(boolean)*: if True, includes `DJ-Database-URL <https://github.com/jacobian/dj-database-url>`__ , a simple Django utility allows you to utilize the 12factor inspired DATABASE_URL environment variable to configure your Django application.

Links
=====

-  Documentation: https://drf-compose.readthedocs.io
-  Changes: https://drf-compose.readthedocs.io/changes/
-  PyPI Releases: https://pypi.org/project/drf-compose/
-  Source Code: https://github.com/IamAbbey/drf_compose
-  Issue Tracker: https://github.com/IamAbbey/drf_compose/issues

Credits
=======

This package was created with
`Cookiecutter <https://github.com/audreyr/cookiecutter>`__ and the
`audreyr/cookiecutter-pypackage <https://github.com/audreyr/cookiecutter-pypackage>`__
project template.
