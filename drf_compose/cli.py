"""Console script for drf_compose."""
import json
import pathlib
import subprocess
import sys

import click
import django
import emoji
import yaml as YAML
from django.conf import settings
from django.template.loader import render_to_string

from drf_compose.django_core import settings as local_settings

settings.configure(
    DEBUG=False,
    INSTALLED_APPS=local_settings.INSTALLED_APPS,
    TEMPLATES=local_settings.TEMPLATES,
    SECRET_KEY=local_settings.SECRET_KEY,
)

django.setup()


@click.command()
@click.option(
    "-s",
    "--source",
    default="drf-compose.json",
    show_default=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        path_type=pathlib.Path,
    ),
    help="Specify an alternate compose file as source",
)
@click.option(
    "--yaml",
    is_flag=True,
    help="Indicates that the supplied source file is a YAML file",
)
def main(source: pathlib.Path, yaml: bool):
    """This script composes a DRF project."""

    click.echo(
        click.style(
            emoji.emojize("Generating DRF Project!... Please wait", use_aliases=True),
            bold=True,
        )
    )

    compose_file_content = source.read_text()
    try:
        if yaml:
            compose_file_content = YAML.full_load(compose_file_content)
        else:
            compose_file_content = json.loads(compose_file_content)
    except Exception as e:
        print(e)
        click.echo("Error parsing compose file", err=True)
        raise click.ClickException("Error parsing compose file")

    project_name = get_key_or_error(
        compose_file_content, "name", "project name is required"
    )
    specified_apps = list(
        map(get_app_names, get_key_or_error(compose_file_content, "app_with_model"))
    )

    if compose_file_content.get("auth_app", None) is not None:
        specified_apps.insert(0, get_app_names(compose_file_content.get("auth_app")))

    new_project_path = pathlib.Path(source.parent / project_name)

    if not new_project_path.exists():
        new_project_path.mkdir(exist_ok=True)
        subprocess.run(
            [
                "django-admin",
                "startproject",
                project_name,
                source.parent / project_name,
            ]
        )
    else:
        raise click.ClickException(
            click.style(
                f"Project folder with the specified project name ({project_name}) already exists.",
                fg="red",
            )
        )

    project_context = {
        "local_apps": specified_apps,
        "project_name": project_name,
        "auth_app": compose_file_content.get("auth_app", None),
    }
    new_project_settings_file = pathlib.Path(
        source.parent / project_name / project_name / "settings.py"
    )
    copy_tpl_files(
        "project_level/settings.py-tpl", new_project_settings_file, project_context
    )

    new_project_urls_file = pathlib.Path(
        source.parent / project_name / project_name / "urls.py"
    )
    copy_tpl_files(
        "project_level/project_urls.py-tpl",
        new_project_urls_file,
        project_context,
        True,
    )

    new_project_requirements_file = pathlib.Path(
        source.parent / project_name / "requirements.txt"
    )
    copy_tpl_files(
        "project_level/requirements.txt-tpl", new_project_requirements_file, {}, True
    )

    apps_path = pathlib.Path(new_project_path / "apps")
    apps_path.mkdir(exist_ok=True)

    pathlib.Path(apps_path / "__init__.py").touch(exist_ok=True)

    for app_with_model in get_key_or_error(compose_file_content, "app_with_model"):
        app_name = get_key_or_error(app_with_model, "app_name")
        app_name_path = apps_path / app_name
        if not pathlib.Path(app_name_path).exists():
            pathlib.Path(app_name_path).mkdir(exist_ok=True)
            subprocess.run(["django-admin", "startapp", app_name, app_name_path])

        new_app_apps_file = pathlib.Path(app_name_path / "apps.py")
        copy_tpl_files("app/apps.py-tpl", new_app_apps_file, {"app_name": app_name})

        models_context = {"models": app_with_model.get("models")}

        if models_context["models"] and type(models_context["models"]) == list:

            # clean models for required fields
            for single_model in models_context["models"]:
                get_key_or_error(single_model, "name", "model's name is required")
                get_key_or_error(
                    single_model, "fields", "model's list of fields is required"
                )
                # clean model fields for required values
                for single_field in single_model["fields"]:
                    get_key_or_error(single_field, "name", "field's name is required")
                    get_key_or_error(single_field, "type", "field's type is required")

            new_app_model_file = pathlib.Path(app_name_path / "models.py")
            copy_tpl_files("app/models.py-tpl", new_app_model_file, models_context)

            new_app_serializers_file = pathlib.Path(app_name_path / "serializers.py")
            copy_tpl_files(
                "app/serializers.py-tpl", new_app_serializers_file, models_context, True
            )

            new_app_views_file = pathlib.Path(app_name_path / "views.py")
            copy_tpl_files("app/views.py-tpl", new_app_views_file, models_context)

            new_app_views_file = pathlib.Path(app_name_path / "admin.py")
            copy_tpl_files("app/admin.py-tpl", new_app_views_file, models_context)

            new_app_urls_file = pathlib.Path(app_name_path / "urls.py")
            copy_tpl_files(
                "app/app_urls.py-tpl", new_app_urls_file, models_context, True
            )

    if compose_file_content.get("auth_app", None) is not None:
        auth_app = compose_file_content.get("auth_app")
        auth_app_name = get_key_or_error(
            auth_app, "app_name", "auth app_name is required"
        )
        auth_app_name_path = apps_path / auth_app_name
        if not pathlib.Path(auth_app_name_path).exists():
            pathlib.Path(auth_app_name_path).mkdir(exist_ok=True)
            subprocess.run(
                ["django-admin", "startapp", auth_app_name, auth_app_name_path]
            )
        get_key_or_error(auth_app, "model_name", "auth model_name is required")

        if auth_app.get("fields") and type(auth_app["fields"]) == list:
            # clean model fields for required values
            for single_field in auth_app["fields"]:
                get_key_or_error(single_field, "name", "field's name is required")
                get_key_or_error(single_field, "type", "field's type is required")

        auth_models_context = {
            "model": auth_app,
            "include": compose_file_content.get("include"),
        }

        new_app_model_file = pathlib.Path(auth_app_name_path / "models.py")
        copy_tpl_files(
            "auth_app/models.py-tpl", new_app_model_file, auth_models_context
        )

        new_app_manager_file = pathlib.Path(auth_app_name_path / "manager.py")
        copy_tpl_files(
            "auth_app/manager.py-tpl", new_app_manager_file, auth_models_context, True
        )

        new_app_serializers_file = pathlib.Path(auth_app_name_path / "serializers.py")
        copy_tpl_files(
            "auth_app/serializers.py-tpl",
            new_app_serializers_file,
            auth_models_context,
            True,
        )

        new_app_views_file = pathlib.Path(auth_app_name_path / "views.py")
        copy_tpl_files("auth_app/views.py-tpl", new_app_views_file, auth_models_context)

        new_app_views_file = pathlib.Path(auth_app_name_path / "admin.py")
        copy_tpl_files("auth_app/admin.py-tpl", new_app_views_file, auth_models_context)

        new_app_urls_file = pathlib.Path(auth_app_name_path / "urls.py")
        copy_tpl_files(
            "auth_app/auth_urls.py-tpl", new_app_urls_file, auth_models_context, True
        )

        new_app_apps_file = pathlib.Path(auth_app_name_path / "apps.py")
        copy_tpl_files(
            "app/apps.py-tpl", new_app_apps_file, {"app_name": auth_app_name}
        )

    subprocess.run(["black", new_project_path, "-q"])
    click.secho(
        emoji.emojize("All done! :sparkles: :cake: :sparkles:", use_aliases=True),
        bold=True,
    )
    sys.exit(0)


def get_app_names(obj: dict, append_apps: bool = True):
    if append_apps:
        return f"apps.{obj['app_name']}"
    return f"{obj['app_name']}"


def copy_tpl_files(
    tpl_file_name: str, dest_file_path: pathlib.Path, context: dict, touch: bool = False
):
    if touch:
        dest_file_path.touch(exist_ok=True)
    render_model = render_to_string(tpl_file_name, context)
    dest_file_path.write_text(render_model)


def get_key_or_error(obj: dict, key: str, err_message=None):
    if key in obj:
        return obj[key]
    raise click.ClickException(
        click.style(err_message if err_message else f"{key} is required", fg="red")
    )


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
