"""Tests for `drf_compose` package."""
import json
import pathlib

import pytest
from click.testing import CliRunner

from drf_compose import cli

test_compose = """
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
              "ordering": ["-content"]
            },
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
                "name": "content",
                "type": "text",
                "options": {
                  "blank": true,
                  "null": true
                }
              }
            ],
            "str": "title"
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
            }
        ],
        "str": "title"
    }
  }
"""


def create_compose_file(content=None):
    pathlib.Path("drf-compose.json").touch(exist_ok=True)
    pathlib.Path("drf-compose.json").write_text(content if content else test_compose)


def test_valid_compose_file():
    """Test the CLI."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        create_compose_file()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0


def test_missing_compose_file():
    """Test the CLI."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli.main)
        print(result.stdout)
        assert result.exception
        assert result.exit_code == 2


@pytest.mark.parametrize(
    "key_to_remove, exit_code",
    [
        ("name", 1),
        ("app_with_model", 1),
        ("", 0),
    ],
)
def test_missing_level_1_required_key(key_to_remove, exit_code):
    runner = CliRunner()
    with runner.isolated_filesystem():
        test_compose_json: dict = json.loads(test_compose)
        test_compose_json.pop(key_to_remove, None)
        create_compose_file(json.dumps(test_compose_json))
        result = runner.invoke(cli.main)
        if exit_code == 1:
            assert result.exception
        assert result.exit_code == exit_code


@pytest.mark.parametrize(
    "parent_key, parent_is_list, key_to_remove, exit_code",
    [
        ("app_with_model", True, "app_name", 1),
        ("app_with_model", True, "", 0),
        ("auth_app", False, "app_name", 1),
        ("auth_app", False, "model_name", 1),
        ("auth_app", False, "", 0),
    ],
)
def test_level_2_required_key(parent_key, parent_is_list, key_to_remove, exit_code):
    runner = CliRunner()
    with runner.isolated_filesystem():
        test_compose_json: dict = json.loads(test_compose)
        if parent_is_list:
            test_compose_json[parent_key][0].pop(key_to_remove, None)
        else:
            test_compose_json[parent_key].pop(key_to_remove, None)
        create_compose_file(json.dumps(test_compose_json))
        result = runner.invoke(cli.main)
        print(result.stdout)
        if exit_code == 1:
            assert result.exception
        assert result.exit_code == exit_code


@pytest.mark.parametrize(
    "ancestor_key, ancestor_is_list, parent_key, parent_is_list, key_to_remove, exit_code",
    [
        ("app_with_model", True, "models", True, "name", 1),
        ("app_with_model", True, "models", True, "fields", 1),
        ("app_with_model", True, "models", True, "", 0),
        ("auth_app", False, "fields", True, "name", 1),
        ("auth_app", False, "fields", True, "type", 1),
        ("auth_app", False, "fields", True, "", 0),
    ],
)
def test_level_3_required_key(
    ancestor_key, ancestor_is_list, parent_key, parent_is_list, key_to_remove, exit_code
):
    runner = CliRunner()
    with runner.isolated_filesystem():
        test_compose_json: dict = json.loads(test_compose)
        if ancestor_is_list:
            ancestor = test_compose_json[ancestor_key][0]
        else:
            ancestor = test_compose_json[ancestor_key]
        if parent_is_list:
            ancestor[parent_key][0].pop(key_to_remove, None)
        else:
            ancestor[parent_key].pop(key_to_remove, None)
        create_compose_file(json.dumps(test_compose_json))
        result = runner.invoke(cli.main)
        print(result.stdout)
        if exit_code == 1:
            assert result.exception
        assert result.exit_code == exit_code


@pytest.mark.parametrize(
    "grand_ancestor_key, grand_ancestor_is_list, ancestor_key, ancestor_is_list, parent_key,"
    + "parent_is_list, key_to_remove, exit_code",
    [
        ("app_with_model", True, "models", True, "fields", True, "name", 1),
        ("app_with_model", True, "models", True, "fields", True, "type", 1),
        ("app_with_model", True, "models", True, "fields", True, "", 0),
    ],
)
def test_level_4_required_key(
    grand_ancestor_key,
    grand_ancestor_is_list,
    ancestor_key,
    ancestor_is_list,
    parent_key,
    parent_is_list,
    key_to_remove,
    exit_code,
):
    runner = CliRunner()
    with runner.isolated_filesystem():
        test_compose_json: dict = json.loads(test_compose)
        if grand_ancestor_is_list:
            grand_ancestor = test_compose_json[grand_ancestor_key][0]
        else:
            grand_ancestor = test_compose_json[grand_ancestor_key]
        if ancestor_is_list:
            ancestor = grand_ancestor[ancestor_key][0]
        else:
            ancestor = grand_ancestor[ancestor_key]
        if parent_is_list:
            ancestor[parent_key][0].pop(key_to_remove, None)
        else:
            ancestor[parent_key].pop(key_to_remove, None)
        create_compose_file(json.dumps(test_compose_json))
        result = runner.invoke(cli.main)
        if exit_code == 1:
            assert result.exception
        assert result.exit_code == exit_code
