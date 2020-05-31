
import os
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

    base_uri = os.getenv('BASE_URI')
    cabinet_uri = os.getenv('CABINET_URI')
    token = os.getenv('ACCESS_TOKEN')
    email = os.getenv('DEVELOPER_EMAIL')
    folder_path = os.getenv('FOLDER_PATH')

    file_ext = ('xlsx', 'xls')

    http_client = BaseApiHandler(base_uri=base_uri, token=token, email=email)

    app = AppHandler(http_client=http_client, folder_path=folder_path, file_ext=file_ext, parse_map=parse_map)
    app.run(statuses_map=STATUSES_MAP)

    print('Parsed successfully. Please open HR cabinet by link: %s' % cabinet_uri)


if __name__ == '__main__':
    main()
