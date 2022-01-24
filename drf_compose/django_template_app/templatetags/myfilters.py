from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name="clean_field_type")
@stringfilter
def clean_field_type(value: str):
    lowercase_value = value.lower()
    return_value = value.capitalize()
    if lowercase_value == "char" or lowercase_value == "text":
        return f"{return_value}Field"
    elif lowercase_value == "url":
        return "URLField"
    elif lowercase_value == "datetime":
        return "DateTimeField"
    elif lowercase_value == "fk":
        return "ForeignKey"
    elif lowercase_value == "m2m":
        return "ManyToManyField"
    elif lowercase_value == "o2o":
        return "OneToOneField"
    return value if "field" in lowercase_value else f"{return_value}Field"


STRING_OPTIONS = [
    "to",
    "related_name",
    "related_query_name",
    "to_field",
    "db_column",
    "help_text",
    "verbose_name",
]


@register.filter(name="clean_option")
@stringfilter
def clean_option(value: str, param: str):
    if param in STRING_OPTIONS:
        return f"'{value}'"
    return value
