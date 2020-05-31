
import os
import argparse
from dotenv import load_dotenv

from src.AppHandler import AppHandler
from src.BaseApiHandler import BaseApiHandler

# ideally provide through json/yaml file or through http
parse_map = {
    'position': {
        'title': 'Должность',
        'normalize': ['make_position']
    },
    'name': {
        'title': 'ФИО',
        'normalize': ['make_name']
    },
    'money': {
        'title': 'Ожидания по ЗП',
        'normalize': ['only_numbers']
    },
    'comment': {
        'title': 'Комментарий',
        'normalize': []
    },
    'status': {
        'title': 'Статус',
        'normalize': ['make_status']
    },
}

STATUSES_MAP = {
    'New Lead': 'New Lead',
    'Submitted': 'Submitted',
    'Отправлено письмо': 'Contacted',
    'Интервью с HR': 'HR Interview',
    'Client Interview': 'Client Interview',
    'Выставлен оффер': 'Offered',
    'Offer Accepted': 'Offer Accepted',
    'Hired': 'Hired',
    'Trial passed': 'Trial passed',
    'Отказ': 'Declined',
}


def main():
    load_dotenv(verbose=True)

    arg_parser = argparse.ArgumentParser(description='')

    arg_parser.add_argument('--base_uri', default=os.getenv('BASE_URI'))
    arg_parser.add_argument('--cabinet_uri', default=os.getenv('CABINET_URI'))
    arg_parser.add_argument('--access_token', default=os.getenv('ACCESS_TOKEN'))
    arg_parser.add_argument('--developer_email', default=os.getenv('DEVELOPER_EMAIL'))
    arg_parser.add_argument('--folder_path', default=os.getenv('FOLDER_PATH'))

    args = arg_parser.parse_args()

    base_uri = args.base_uri
    cabinet_uri = args.cabinet_uri
    token = args.access_token
    email = args.developer_email
    folder_path = args.folder_path

    if not base_uri or not cabinet_uri or not token or not email or not folder_path:
        print('You must provide required configuration parameters')
        exit(arg_parser.print_usage())

    file_ext = ('xlsx', 'xls')

    http_client = BaseApiHandler(base_uri=base_uri, token=token, email=email)

    app = AppHandler(http_client=http_client, folder_path=folder_path, file_ext=file_ext, parse_map=parse_map)
    app.run(statuses_map=STATUSES_MAP)

    print('Parsed successfully. Please open HR cabinet by link: %s' % cabinet_uri)


if __name__ == '__main__':
    main()