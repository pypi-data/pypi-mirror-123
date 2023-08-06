"""
Модуль для работы с конфигурацией из командной строки
"""
from sys import argv
from os import getenv
from os.path import exists as path_exists
from json import dumps as json_dump, loads as json_load
import argparse
from config import __version__

new_element = None


def __parse_element__(element, name_parent_element, parent_element):
    global new_element
    if element['type'] == 'object':
        parent_element[name_parent_element] = {}
        parent_element = parent_element[name_parent_element]
        for i in element['required']:
            __parse_element__(element['properties'][i], i, parent_element)
    else:
        parent_element[name_parent_element] = element.get('default')


def create_command(params):
    default_config = {
        "logging": {
            "level_logging": "ERROR",
            "format_logging": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "handlers": [
                {
                    "type_handler": "file",
                    "level_logging": "ERROR",
                    "directory_log": "logs",
                    "logging_rotation_type": "TIMED",
                    "backup_count": 1,
                    "logging_interval": "d 1"
                },
                {
                    "enabled_handler": False,
                    "type_handler": "db",
                    "level_logging": "ERROR"
                },
                {
                    "type_handler": "console",
                    "level_logging": "ERROR"
                }
            ],
            "settings_overload": [
                {
                    "name_logger": "General",
                    "settings": {
                        "handlers": [
                            {
                                "enabled_handler": True,
                                "type_handler": "file",
                                "directory_log": "logs",
                                "logging_rotation_type": "TIMED",
                                "backup_count": 1,
                                "logging_interval": "d 1"
                            }
                        ]
                    }
                }
            ]
        }
    }

    if params.list_elements:
        if not getenv('TEMPLATE_CONFIG', default=None):
            print("Не определена переменная окружения TEMPLATE_CONFIG")
            return

        template = json_load(open(getenv("TEMPLATE_CONFIG")).read())

        message = "Список доступных элементов: "
        for i in template['properties']:
            message += f"{i}, "
        print(message[:-2])
        return

    if path_exists(params.config_file.name):
        print('Файл конфигурации уже существует, перезаписать его? (y/n)')
        answer = input()
        if answer.lower() != "yes" and answer.lower() != 'y':
            return
    if params.elements:
        if not getenv('TEMPLATE_CONFIG', default=None):
            print("Не определена переменная окружения TEMPLATE_CONFIG")
            return

        template = json_load(open(getenv("TEMPLATE_CONFIG")).read())

        for i in params.elements:
            if i not in template['properties']:
                print(f'Элемента {i} нет в шаблоне')
                return
            global new_element
            new_element = {}
            __parse_element__(template['properties'][i], i, new_element)
            default_config[i] = new_element[i]

    params.config_file.write(json_dump(default_config, indent=4))
    print('Конфигурация создана')


methods = {
    "create": create_command
}


def create_parse():
    parser = argparse.ArgumentParser(add_help=False)

    parent_group = parser.add_argument_group(title="Параметры")
    parent_group.add_argument('--version', action='version', help='Вывести номер версии',
                              version='%(prog)s {}'.format(__version__))
    parent_group.add_argument("--help", "-h", action="help", help="Справка")

    subparsers = parser.add_subparsers(dest="command", title="Возможные команды",
                                       description="Команды, которые должны быть в качестве первого параметра %(prog)s")

    create_command_parser = subparsers.add_parser("create", add_help=False)
    create_command_parser.add_argument('config_file', type=argparse.FileType(mode='w'))
    create_command_parser.add_argument('-e', '--elements', nargs='+', help="Элементы, которые нужно добавить в конфиг. "
                                                                           "Для работы этого параметра требуется "
                                                                           "указать переменную окружения "
                                                                           "TEMPLATE_CONFIG")
    create_command_parser.add_argument('--list-elements', action='store_true', default=False)
    create_command_parser.add_argument('-h', '--help', action='help', help='Справка')

    return parser


if __name__ == '__main__':
    parser = create_parse()
    parsed_params = parser.parse_args(argv[1:])

    methods[parsed_params.command](parsed_params)
