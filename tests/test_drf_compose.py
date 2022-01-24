"""Tests for `drf_compose` package."""
import json
import pathlib

import pytest
from click.testing import CliRunner

from drf_compose import cli

from .test_compose_contents import json_test_compose, yaml_test_compose


def create_compose_file(content=None, use_json=True):
    if use_json:
        pathlib.Path("drf-compose.json").touch(exist_ok=True)
        pathlib.Path("drf-compose.json").write_text(
            content if content else json_test_compose
        )
    else:
        pathlib.Path("drf-compose.yaml").touch(exist_ok=True)
        pathlib.Path("drf-compose.yaml").write_text(
            content if content else yaml_test_compose
        )


def test_valid_json_compose_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        create_compose_file()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0


def test_valid_yaml_compose_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        create_compose_file(use_json=False)
        result = runner.invoke(cli.main, args="-s drf-compose.yaml  --yaml")
        assert result.exit_code == 0


def test_project_folder_already_exist():
    runner = CliRunner()
    with runner.isolated_filesystem():
        create_compose_file()
        result = runner.invoke(cli.main)
        result = runner.invoke(cli.main)
        assert result.exception
        assert result.exit_code == 1


def test_error_parsing_compose_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        create_compose_file(content="{")
        result = runner.invoke(cli.main)
        assert result.exception
        assert result.exit_code == 1


def test_missing_compose_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli.main)
        print(result.stdout)
        assert result.exception
        assert result.exit_code == 2


def test_invalid_option_type():
    # e.g app_with_model is expected to be a list
    runner = CliRunner()
    with runner.isolated_filesystem():
        test_compose_json: dict = json.loads(json_test_compose)
        test_compose_json["app_with_model"] = "a string instead of a list"
        create_compose_file(json.dumps(test_compose_json))
        result = runner.invoke(cli.main)
        assert result.exception
        assert result.exit_code == 1


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
        test_compose_json: dict = json.loads(json_test_compose)
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
        test_compose_json: dict = json.loads(json_test_compose)
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
        test_compose_json: dict = json.loads(json_test_compose)
        if ancestor_is_list:
            ancestor = test_compose_json[ancestor_key][0]
        else:
            ancestor = test_compose_json[ancestor_key]
        if parent_is_list:
            ancestor[parent_key][0].pop(key_to_remove, None)
        else:
            ancestor[parent_key].pop(key_to_remove, None)  # pragma: no cover
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
        test_compose_json: dict = json.loads(json_test_compose)
        if grand_ancestor_is_list:
            grand_ancestor = test_compose_json[grand_ancestor_key][0]
        else:
            grand_ancestor = test_compose_json[grand_ancestor_key]  # pragma: no cover
        if ancestor_is_list:
            ancestor = grand_ancestor[ancestor_key][0]
        else:
            ancestor = grand_ancestor[ancestor_key]  # pragma: no cover
        if parent_is_list:
            ancestor[parent_key][0].pop(key_to_remove, None)
        else:
            ancestor[parent_key].pop(key_to_remove, None)  # pragma: no cover
        create_compose_file(json.dumps(test_compose_json))
        result = runner.invoke(cli.main)
        if exit_code == 1:
            assert result.exception
        assert result.exit_code == exit_code
