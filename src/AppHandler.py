
import json
import os
from mimetypes import MimeTypes

from src.XLSParser import XLSParser
from src.utils import get_files_by_ext, get_files_by_filename, is_folder_exists, get_in_path
from src.NormalizeHandler import NormalizeHandler

mime = MimeTypes()


def make_response(func):
    def wrapper(http_client, *args):
        response = func(http_client, *args)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise Exception('Invalid credentials')

        raise Exception('Unhandled server error')

    return wrapper


def make_resume_data(func):
    applicant_map = {
        'last_name': ['fields', 'name', 'last'],
        'first_name': ['fields', 'name', 'first'],
        'middle_name': ['fields', 'name', 'middle'],
        'phone': ['fields', 'phones', 0],
        'email': ['fields', 'email'],
        'position': ['fields', 'experience', 0, 'position'],
        'company': ['fields', 'experience', 0, 'company'],
        'money': ['fields', 'salary'],
        'birthday_day': ['fields', 'birthdate', 'day'],
        'birthday_month': ['fields', 'birthdate', 'month'],
        'birthday_year': ['fields', 'birthdate', 'year'],
        'photo': ['photo', 'id']
    }

    def wrapper(http_client, *args):
        response = func(http_client, *args)
        result = {}

        for k, v in applicant_map.items():
            result[k] = get_in_path(v, response)

        return {
            'original': response,
            'prepared': result
        }

    return wrapper


def normalize_statuses(func):
    def wrapper(http_client, *args):
        response = func(http_client, *args).get('items')
        result = {}

        for status in response:
            result[status.get('name')] = status.get('id')

        return result

    return wrapper


class AppHandler:
    def __init__(self, http_client=None, folder_path=None, file_ext=(), parse_map=None):

        if not is_folder_exists(folder_path):
            raise Exception('%s dir is not exists' % folder_path)

        if not http_client:
            raise Exception('http_client is not provided')

        if not file_ext:
            raise Exception('Extensions list is empty')

        if not parse_map:
            raise Exception('You must provide parse_map')

        self.http_client = http_client
        self.folder_path = folder_path
        self.file_ext = file_ext
        self.parse_map = parse_map
        self.normalizer = None

    @make_response
    def get_account(self):
        return self.http_client.request('GET', '/accounts')

    @make_response
    def get_vacancy_list(self, account_id):
        return self.http_client.request('GET', '/account/%s/vacancies' % account_id)

    @make_response
    def save_applicant(self, account_id, data):
        return self.http_client.request('POST', '/account/%s/applicants' % account_id, data=data)

    @normalize_statuses
    @make_response
    def get_statuses(self, account_id):
        return self.http_client.request('GET', '/account/%s/vacancy/statuses' % account_id)

    @make_resume_data
    @make_response
    def upload_file(self, account_id, files):
        headers = {
            'X-File-Parse': 'true',
        }

        return self.http_client.request('POST', '/account/%s/upload' % account_id, files=files, headers=headers)

    @make_response
    def add_to_vacancy(self, account_id, applicant_id, data):
        return self.http_client.request('POST', '/account/%s/applicants/%s/vacancy' % (account_id, applicant_id),
                                        data=data)

    def run(self, statuses_map):

        account = self.get_account().get('items')[0]
        account_id = account.get('id')

        vacancy_list = self.get_vacancy_list(account_id).get('items')
        status_list = self.get_statuses(account_id)

        self.normalizer = NormalizeHandler(status_list, vacancy_list, statuses_map)

        xls_parser = XLSParser(self.parse_map, self.normalizer)

        files = get_files_by_ext(self.folder_path, self.file_ext)

        # TODO: think about parallel executing
        for file in files:
            items = xls_parser.run(os.path.join(self.folder_path, file))

            for item in items:
                resume_name = item.get('position').get('title')
                if not resume_name:
                    continue

                resume_list = get_files_by_filename(
                    os.path.join(self.folder_path, ),
                    item.get('name').get('full_name')
                )

                prepared_resume = None
                externals = []

                for resume in resume_list:
                    full_path = os.path.join(resume.get('path'), resume.get('name'))
                    mime_type = mime.guess_type(full_path)

                    fd = open(full_path, 'rb')
                    file = {'file': (os.path.basename(full_path), fd, mime_type[0])}

                    resume_data = self.upload_file(account_id, file)

                    fd.close()

                    original_resume = resume_data.get('original')

                    prepared_resume = resume_data.get('prepared')
                    prepared_resume['money'] = item.get('money')

                    externals.append({
                        'data': {
                            'body': get_in_path(['text'], original_resume),
                        },
                        'files': [
                            {
                                'id': get_in_path(['id'], original_resume),
                            }
                        ],
                        'auth_type': 'NATIVE',
                        'account_source': None
                    })

                prepared_resume['externals'] = externals
                applicant = self.save_applicant(account_id, json.dumps(prepared_resume))

                # is_declined = status_list['Declined'] == get_in_path(['status'], item)
                data = {
                    'vacancy': get_in_path(['position', 'id'], item),
                    'status': get_in_path(['status'], item),
                    'comment': get_in_path(['comment'], item),
                    'files': list(map(lambda el: get_in_path(['files', 0, 'id'], el), externals)),
                    # 'rejection_reason': get_in_path(['comment'], item) if is_declined else None
                    'rejection_reason': None  # api всегда отвечает 400 если не None
                }

                self.add_to_vacancy(account_id, applicant.get('id'), json.dumps(data))
