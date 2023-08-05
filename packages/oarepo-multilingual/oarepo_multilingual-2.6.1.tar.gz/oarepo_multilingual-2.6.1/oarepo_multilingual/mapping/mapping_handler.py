# -*- coding: utf-8 -*- #
"""Simple test of version import."""


def replace_lang_placeholder(value, language):
    if isinstance(value, dict):
        return {k: replace_lang_placeholder(v, language) for k, v in value.items()}
    elif isinstance(value, (list, tuple)):
        return [replace_lang_placeholder(_, language) for _ in value]
    elif isinstance(value, str):
        return value.replace("*", language)
    else:
        return value


def handler(type=None, resource=None, id=None, json_pointer=None,
            app=None, content=None, root=None, content_pointer=None):
    """Use this function as handler."""
    languages = list(app.config.get("MULTILINGUAL_SUPPORTED_LANGUAGES", []))

    default_template = app.config.get("ELASTICSEARCH_DEFAULT_LANGUAGE_TEMPLATE", {})
    templates = app.config.get("ELASTICSEARCH_LANGUAGE_TEMPLATES", {})

    data_dict = dict()
    for language in languages:
        if id is not None:
            language_with_context = language + '#' + id
            if language_with_context in templates.keys() or f"*#{id}" in templates.keys():
                template = templates.get(language_with_context) or templates.get(f"*#{id}")
                data_dict[language] = replace_lang_placeholder(template,
                                                               language)
                continue
        data_dict[language] = replace_lang_placeholder(templates.get(language, default_template),
                                                       language)

    return {
        "type": "object",
        "properties": data_dict
    }
