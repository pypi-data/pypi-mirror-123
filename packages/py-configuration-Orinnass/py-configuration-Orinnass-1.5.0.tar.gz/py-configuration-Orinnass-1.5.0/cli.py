"""
Модуль для работы с конфигурацией из командной строки
"""
from sys import argv
from os.path import exists as path_exists
from json import dumps as json_dump
import argparse
from config import __version__


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

    if path_exists(params.config_file.name):
        print('Файл конфигурации уже существует, перезаписать его? (y/n)')
        answer = input()
        if answer.lower() != "yes" and answer.lower() != 'y':
            return

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
    create_command_parser.add_argument('-h', '--help', action='help', help='Справка')

    return parser


if __name__ == '__main__':
    parser = create_parse()
    parsed_params = parser.parse_args(argv[1:])

    methods[parsed_params.command](parsed_params)
