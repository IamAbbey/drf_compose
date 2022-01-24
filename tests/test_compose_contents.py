json_test_compose = """
{
  "name": "delight_blog",
  "app_with_model": [
    {
      "app_name": "post",
      "models": [
        {
          "name": "Post",
          "meta": {
            "verbose_name": "Post",
            "verbose_name_plural": "Posts",
            "ordering": ["-created_date"]
          },
          "use_uuid_as_key": true,
          "fields": [
            {
              "name": "title",
              "type": "char",
              "options": {
                "blank": true,
                "null": true,
                "help_text": "This is the post title",
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
            },
            {
              "name": "created_date",
              "type": "dateTime",
              "options": {
                "auto_now_add": true
              }
            },
            {
              "name": "created_by",
              "type": "fk",
              "options": {
                "to": "authentication.CustomUser",
                "on_delete": "models.CASCADE"
              }
            },
            {
              "name": "categories",
              "type": "m2m",
              "options": {
                "to": "category.Category"
              }
            }
          ],
          "str": "title"
        }
      ]
    },
    {
      "app_name": "category",
      "models": [
        {
          "name": "Category",
          "meta": {
            "verbose_name": "Category",
            "verbose_name_plural": "Categories",
            "ordering": ["-created_date"]
          },
          "fields": [
            {
              "name": "name",
              "type": "char",
              "options": {
                "help_text": "This is the name of the category",
                "max_length": 200
              }
            },
            {
              "name": "created_date",
              "type": "dateTime",
              "options": {
                "auto_now_add": true
              }
            },
            {
              "name": "label",
              "type": "o2o",
              "options": {
                "to": "Label",
                "primary_key": true,
                "on_delete": "models.CASCADE"
              }
            }
          ],
          "str": "name"
        },
        {
          "name": "Label",
          "meta": {
            "ordering": ["-created_date"]
          },
          "use_uuid_as_key": true,
          "fields": [
            {
              "name": "name",
              "type": "char",
              "options": {
                "help_text": "This is the name of the label",
                "max_length": 200
              }
            },
            {
              "name": "created_date",
              "type": "dateTime",
              "options": {
                "auto_now_add": true
              }
            }
          ],
          "str": "name"
        }
      ]
    }
  ],
  "auth_app": {
    "app_name": "authentication",
    "model_name": "CustomUser",
    "meta": {
      "verbose_name": "CustomUser",
      "verbose_name_plural": "CustomUsers",
      "ordering": ["-id"]
    },
    "username_field": "email",
    "required_fields": ["phone"],
    "use_uuid_as_key": true,
    "fields": [
      {
        "name": "title",
        "type": "char",
        "options": {
          "blank": true,
          "null": true,
          "max_length": 200
        }
      },
      {
        "name": "email",
        "type": "email",
        "options": {
          "unique": true,
          "max_length": 200
        }
      },
      {
        "name": "phone",
        "type": "char",
        "options": {
          "max_length": 15,
          "blank": true,
          "null": true
        }
      },
      {
        "name": "twitter_url",
        "type": "url",
        "options": {
          "blank": true,
          "null": true
        }
      }
    ],
    "str": "title"
  }
}
"""

yaml_test_compose = """
---
name: delight_blog
app_with_model:
- app_name: post
  models:
  - name: Post
    meta:
      verbose_name: Post
      verbose_name_plural: Posts
      ordering:
      - "-created_date"
    use_uuid_as_key: true
    fields:
    - name: title
      type: char
      options:
        blank: true
        'null': true
        help_text: This is the post title
        max_length: 200
    - name: content
      type: text
      options:
        blank: true
        'null': true
    - name: created_date
      type: dateTime
      options:
        auto_now_add: true
    - name: created_by
      type: fk
      options:
        to: authentication.CustomUser
        on_delete: models.CASCADE
    - name: categories
      type: m2m
      options:
        to: category.Category
    str: title
- app_name: category
  models:
  - name: Category
    meta:
      verbose_name: Category
      verbose_name_plural: Categories
      ordering:
      - "-created_date"
    fields:
    - name: name
      type: char
      options:
        help_text: This is the name of the category
        max_length: 200
    - name: created_date
      type: dateTime
      options:
        auto_now_add: true
    - name: label
      type: o2o
      options:
        to: Label
        primary_key: true
        on_delete: models.CASCADE
    str: name
  - name: Label
    meta:
      ordering:
      - "-created_date"
    use_uuid_as_key: true
    fields:
    - name: name
      type: char
      options:
        help_text: This is the name of the label
        max_length: 200
    - name: created_date
      type: dateTime
      options:
        auto_now_add: true
    str: name
auth_app:
  app_name: authentication
  model_name: CustomUser
  meta:
    verbose_name: CustomUser
    verbose_name_plural: CustomUsers
    ordering:
    - "-id"
  username_field: email
  required_fields:
  - phone
  use_uuid_as_key: true
  fields:
  - name: title
    type: char
    options:
      blank: true
      'null': true
      max_length: 200
  - name: email
    type: email
    options:
      unique: true
      max_length: 200
  - name: phone
    type: char
    options:
      max_length: 15
      blank: true
      'null': true
  - name: twitter_url
    type: url
    options:
      blank: true
      'null': true
  str: title

"""
