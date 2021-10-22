## DRF Compose
----------------

<!-- .. .. image:: https://img.shields.io/pypi/v/drf_compose.svg
..         :target: https://pypi.python.org/pypi/drf_compose

.. .. image:: https://img.shields.io/travis/IamAbbey/drf_compose.svg
..         :target: https://travis-ci.com/IamAbbey/drf_compose

.. .. image:: https://readthedoc
..         :target: https://drf-compose.readthedocs.io/en/latest/?version=latest
..         :alt: Documentation Status


.. .. image:: https://pyup.io/repos/github/IamAbbey/drf_compose/shield.svg
..      :target: https://pyup.io/repos/github/IamAbbey/drf_compose/
..      :alt: Updates -->


DRF Compose is a Python package for defining and quick starting Django Rest Framework projects. 
With DRF Compose,  you use a JSON or YAML file to configure your DRF application. 
Then, with a single command, you get to generate your DRF project code using all the specified configuration from your compose file. 
To learn more about all the features of DRF Compose, see the list of features below.

DRF Compose is aimed at making the process of starting a DRF project quick and fun while also preventing any frustration caused by the inability to quick start an API.


Installing
----------
Install and update using [pip]:

    $ pip install -U drf_compose

[pip]: https://pip.pypa.io/en/stable/getting-started/


Usage
--------
Using DRF Compose is basically a two-step process:

- Define your application in a drf-compose.yml.

- Run drf-compose and the DRF compose command generates a ready to use DRF project code.

A drf-compose file looks like this:

<!-- #### In JSON format:
---------------- -->

<!-- ```json
{
  "name": "delight_blog",
  "app_with_model": [
    {
      "app_name": "post",
      "models": [
        {
          "name": "Post",
          "fields": {
            "title": {
              "type": "char",
              "blank": true,
              "null": true,
              "max_length": 200
            },
            "content": {
              "type": "text",
              "blank": true,
              "null": true
            }
          },
          "str": "title"
        },
        {
          "name": "Category",
          "fields": {
            "title": {
              "type": "char",
              "blank": true,
              "null": true,
              "max_length": 200
            }
          }
        }
      ]
    }
  ]
}
``` -->

<table style="width:100%;">
<tr>
<td> In YAML format (.yml) </td> <td> In JSON format (.json) </td>
</tr>
<tr>
<td>

```yaml
---
  name: delight_blog
  app_with_model:
  - app_name: post
    models:
    - name: Post
      fields:
      - name: title
        type: char
        blank: true
        'null': true
        max_length: 200
      - name: content
        type: text
        blank: true
        'null': true
      str: title
    - name: Category
      fields:
      - name: name
        type: char
        blank: true
        'null': true
        max_length: 200

```
</td>
<td>

```json
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
              "blank": true,
              "null": true,
              "max_length": 200
            },
            {
              "name": "content",
              "type": "text",
              "blank": true,
              "null": true
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
              "blank": true,
              "null": true,
              "max_length": 200
            }
          ]
        }
      ]
    }
  ]
}
```
</td>
</tr>
</table>

<!-- 
#### In yaml format:
---------------- -->

<!-- ```yaml
name: delight_blog
app_with_model:
- app_name: post
  models:
  - name: Post
    fields:
      title:
        type: char
        blank: true
        'null': true
        max_length: 200
      content:
        type: text
        blank: true
        'null': true
    str: title
  - name: Category
    fields:
      title:
        type: char
        blank: true
        'null': true
        max_length: 200

``` -->

Options
--------
1. `name`: specifies the project name
2. `app_with_model`: a list consisting app details describing the apps in the DRF project
   - `app_name`: specifies the app name
   - `models`: a list of models belonging to the app
      - `name`: specifies the model name
      - `meta`: specifies the different model meta options as in the [Django model meta documentation](https://docs.djangoproject.com/en/3.2/topics/db/models/#meta-options)
      - `fields`: a list of fields belonging to a model.
        - `name` (*required*): the name of the field as in the [Django model field documentation] (https://docs.djangoproject.com/en/3.2/topics/db/models/#fields).
        - `type` (*required*): the field type as specified in [Django model field type reference documentation](https://docs.djangoproject.com/en/3.2/ref/models/fields/#model-field-types). Basic syntax sugar also supported as shown below:
            | Syntax      | Field Type |
            | ----------- | ----------- |
            | char      | CharField       |
            | text      | TextField       |
            | fk      | ForeignKey       |
            | o2o   | OneToOneField        |
            | m2m   | ManyToManyField        |
        - `options`: specifies field option as in the [Django model field documentation](https://docs.djangoproject.com/en/3.2/ref/models/fields/).
      - `use_uuid_as_key` (*boolean*): if True, a UUID is used as the model's primary key.
      - `str`: specifies the field to be returned as representation of the model in `__str__`. **Must be one of the specified field names**
        

Links
-----

-   Documentation: https://drf-compose.readthedocs.io
-   Changes: https://drf-compose.readthedocs.io/changes/
-   PyPI Releases: https://pypi.org/project/drf-compose/
-   Source Code: https://github.com/IamAbbey/drf_compose
-   Issue Tracker: https://github.com/IamAbbey/drf_compose/issues


Credits
-------

This package was created with [Cookiecutter][_Cookiecutter] and the [audreyr/cookiecutter-pypackage][_cookiecutter-pypackage] project template.

[_Cookiecutter]: https://github.com/audreyr/cookiecutter
[_cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage
