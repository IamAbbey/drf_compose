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

# Configure django.conf settings default values to use this project local_settings
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

    # Read the specified source file content, default is drf-compose.json in the current working directory.
    compose_file_content = source.read_text()

    # Try parsing the read file content, raise an error if there was an error parsing the file's content.
    try:
        if yaml:
            # If the --yaml flag is specified, it parses the file's content as YAML.
            compose_file_content = YAML.full_load(compose_file_content)
        else:
            # If the --yaml flag is not specified (which is the default), it parses the file's content as JSON.
            compose_file_content = json.loads(compose_file_content)
    except Exception:
        click.echo("Error parsing compose file", err=True)
        raise click.ClickException("Error parsing compose file")

    # Get the specified project name, raise an error if not found.
    project_name = get_key_or_error(
        compose_file_content, "name", err_message="project name is required"
    )

    # Get the list of specified project application names
    specified_apps = list(
        map(
            get_app_names,
            get_key_or_error(compose_file_content, "app_with_model", content_type=list),
        )
    )

    # Since auth_app is optional, get the specified application name if there exist auth_app
    if compose_file_content.get("auth_app", None) is not None:
        specified_apps.insert(0, get_app_names(compose_file_content.get("auth_app")))

    # Construct the project path using the source file parent directory and project name
    new_project_path = pathlib.Path(source.parent / project_name)

    if not new_project_path.exists():
        # If the project path does not exist, create it and run the django-admin startproject <project_name> command
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

    # Project level template files are files in the generated project directory by django e.g settings.py, urls.py
    project_context = {
        "local_apps": specified_apps,
        "project_name": project_name,
        "auth_app": compose_file_content.get("auth_app", None),
    }

    # Construct path to settings.py
    new_project_settings_file = pathlib.Path(
        source.parent / project_name / project_name / "settings.py"
    )
    # Write into settings.py using the settings.py-tpl template file and project_context
    copy_tpl_files(
        "project_level/settings.py-tpl", new_project_settings_file, project_context
    )

    # Construct path to urls.py
    new_project_urls_file = pathlib.Path(
        source.parent / project_name / project_name / "urls.py"
    )
    # Write into urls.py (create if it does not exist) using the project_urls.py-tpl template file and project_context
    copy_tpl_files(
        "project_level/project_urls.py-tpl",
        new_project_urls_file,
        project_context,
        True,
    )

    # Construct path to requirements.txt
    new_project_requirements_file = pathlib.Path(
        source.parent / project_name / "requirements.txt"
    )
    # Write into requirements.txt (create if it does not exist)
    # using the requirements.txt-tpl template file with no context
    copy_tpl_files(
        "project_level/requirements.txt-tpl", new_project_requirements_file, {}, True
    )

    # Construct path for the apps directory - this is where all the project's applications will reside
    apps_path = pathlib.Path(new_project_path / "apps")
    apps_path.mkdir(exist_ok=True)

    pathlib.Path(apps_path / "__init__.py").touch(exist_ok=True)

    for app_with_model in get_key_or_error(
        compose_file_content, "app_with_model", content_type=list
    ):
        app_name = get_key_or_error(app_with_model, "app_name")
        app_name_path = apps_path / app_name
        if not pathlib.Path(app_name_path).exists():
            # If the application path does not exist, create it and run the django-admin startapp <app_name> command
            pathlib.Path(app_name_path).mkdir(exist_ok=True)
            subprocess.run(["django-admin", "startapp", app_name, app_name_path])

        # Construct path to application specific apps.py
        new_app_apps_file = pathlib.Path(app_name_path / "apps.py")
        # Write into apps.py using the apps.py-tpl template file and application name as context
        copy_tpl_files("app/apps.py-tpl", new_app_apps_file, {"app_name": app_name})

        models_context = {"models": app_with_model.get("models")}

        if models_context["models"] and type(models_context["models"]) == list:

            # clean models for required fields
            for single_model in models_context["models"]:
                get_key_or_error(
                    single_model, "name", err_message="model's name is required"
                )
                get_key_or_error(
                    single_model,
                    "fields",
                    err_message="model's list of fields is required",
                )
                # clean model fields for required values
                for single_field in single_model["fields"]:
                    get_key_or_error(
                        single_field, "name", err_message="field's name is required"
                    )
                    get_key_or_error(
                        single_field, "type", err_message="field's type is required"
                    )

            # Construct file path to application specific models.py and write into it
            new_app_model_file = pathlib.Path(app_name_path / "models.py")
            copy_tpl_files("app/models.py-tpl", new_app_model_file, models_context)

            # Construct file path to application specific serializers.py and write into it
            new_app_serializers_file = pathlib.Path(app_name_path / "serializers.py")
            copy_tpl_files(
                "app/serializers.py-tpl", new_app_serializers_file, models_context, True
            )

            # Construct file path to application specific views.py and write into it
            new_app_views_file = pathlib.Path(app_name_path / "views.py")
            copy_tpl_files("app/views.py-tpl", new_app_views_file, models_context)

            # Construct file path to application specific admin.py and write into it
            new_app_views_file = pathlib.Path(app_name_path / "admin.py")
            copy_tpl_files("app/admin.py-tpl", new_app_views_file, models_context)

            # Construct file path to application specific urls.py and write into it
            new_app_urls_file = pathlib.Path(app_name_path / "urls.py")
            copy_tpl_files(
                "app/app_urls.py-tpl", new_app_urls_file, models_context, True
            )

    if compose_file_content.get("auth_app", None) is not None:
        auth_app = compose_file_content.get("auth_app")
        auth_app_name = get_key_or_error(
            auth_app, "app_name", err_message="auth app_name is required"
        )
        auth_app_name_path = apps_path / auth_app_name

        if not pathlib.Path(auth_app_name_path).exists():
            # If the custom authentication application path does not exist,
            # create it and run the django-admin startapp <app_name> command
            pathlib.Path(auth_app_name_path).mkdir(exist_ok=True)
            subprocess.run(
                ["django-admin", "startapp", auth_app_name, auth_app_name_path]
            )

        get_key_or_error(
            auth_app, "model_name", err_message="auth model_name is required"
        )

        if auth_app.get("fields") and type(auth_app["fields"]) == list:
            # clean model fields for required values
            for single_field in auth_app["fields"]:
                get_key_or_error(
                    single_field, "name", err_message="field's name is required"
                )
                get_key_or_error(
                    single_field, "type", err_message="field's type is required"
                )

        auth_models_context = {
            "model": auth_app,
            "include": compose_file_content.get("include"),
        }

        # Construct file path to custom authentication (user) models.py and write into it
        new_app_model_file = pathlib.Path(auth_app_name_path / "models.py")
        copy_tpl_files(
            "auth_app/models.py-tpl", new_app_model_file, auth_models_context
        )

        # Construct file path to custom authentication (user) manager.py and write into it
        new_app_manager_file = pathlib.Path(auth_app_name_path / "manager.py")
        copy_tpl_files(
            "auth_app/manager.py-tpl", new_app_manager_file, auth_models_context, True
        )

        # Construct file path to custom authentication (user) serializers.py and write into it
        new_app_serializers_file = pathlib.Path(auth_app_name_path / "serializers.py")
        copy_tpl_files(
            "auth_app/serializers.py-tpl",
            new_app_serializers_file,
            auth_models_context,
            True,
        )

        # Construct file path to custom authentication (user) views.py and write into it
        new_app_views_file = pathlib.Path(auth_app_name_path / "views.py")
        copy_tpl_files("auth_app/views.py-tpl", new_app_views_file, auth_models_context)

        # Construct file path to custom authentication (user) admin.py and write into it
        new_app_views_file = pathlib.Path(auth_app_name_path / "admin.py")
        copy_tpl_files("auth_app/admin.py-tpl", new_app_views_file, auth_models_context)

        # Construct file path to custom authentication (user) urls.py and write into it
        new_app_urls_file = pathlib.Path(auth_app_name_path / "urls.py")
        copy_tpl_files(
            "auth_app/auth_urls.py-tpl", new_app_urls_file, auth_models_context, True
        )

        # Construct file path to custom authentication (user) apps.py and write into it
        new_app_apps_file = pathlib.Path(auth_app_name_path / "apps.py")
        copy_tpl_files(
            "app/apps.py-tpl", new_app_apps_file, {"app_name": auth_app_name}
        )

    # Having successfully generated the DRF project code, run black to format the code
    subprocess.run(["black", new_project_path, "-q"])

    # Show success status to user
    click.secho(
        emoji.emojize("All done! :sparkles: :cake: :sparkles:", use_aliases=True),
        bold=True,
    )
    sys.exit(0)


def get_app_names(obj: dict):
    """
    Composes the specified applications name in the form of
    apps.<app_name>
    """
    return f"apps.{obj['app_name']}"


def copy_tpl_files(
    tpl_file_name: str, dest_file_path: pathlib.Path, context: dict, touch: bool = False
):
    """
    This creates a file in the destination path if directed to do so,
    Load a template and render it with a context, and
    finally writes the returned render string to the file.
    """
    if touch:
        dest_file_path.touch(exist_ok=True)
    render_model = render_to_string(tpl_file_name, context)
    dest_file_path.write_text(render_model)


def get_key_or_error(
    obj: dict,
    key: str,
    err_message=None,
    content_type=None,
):
    """
    This checks for a compulsory key in an object and raises
    an error message when the key is not found.

    If content_type is specified it checks if the found value is of the specified type
    if it is not, it raises an error.
    """
    if key in obj:
        if content_type is None:
            return obj[key]
        else:
            if type(obj[key]) == content_type:
                return obj[key]
            else:
                raise click.ClickException(
                    click.style(f"{key} is expected to be a {content_type}", fg="red")
                )
    raise click.ClickException(
        click.style(err_message if err_message else f"{key} is required", fg="red")
    )


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
