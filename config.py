import json
import os

lang_dict = json.load(open('language.json', 'r'))
setup_data = json.load(open('setup.json', 'r'))


def load_setup_data():
    return setup_data


def get_submissions_dir():
    return load_setup_data()['directory']


def get_author():
    name = load_setup_data()['name']
    email = load_setup_data()['email']
    return '{name} <{email}>'.format(name=name, email=email)


def get_language_extension(lang_name):
    if lang_name not in lang_dict.keys():
        raise ValueError("Please provide correct file extension for the language " + lang_name +
                         " in language.json file")
    return lang_dict[lang_name]


def load_submissions_data(path):
    if not os.path.exists(path):
        open(path, 'w').write("{}")
    return json.load(open(path, 'r'))


def write_submissions_data(path, submissions):
    json.dump(obj=submissions, sort_keys=True, indent=2, fp=open(path, 'w'))
