
import re

from src.utils import compose


class NormalizeHandler:
    def __init__(self, statuses, vacancy_list, statuses_map):
        self.statuses_map = statuses_map
        self.statuses = statuses
        self.vacancy_list = vacancy_list

    def get_numbers(self, s):
        return "".join(re.findall(r'\b\d+\b', s))

    def get_status(self, status_name):
        status_key = self.statuses_map.get(status_name)
        return self.statuses.get(status_key)

    def make_position(self, s):
        for vacancy in self.vacancy_list:
            if vacancy.get('position') == s:
                return {
                    'title': vacancy.get('position'),
                    'id': vacancy.get('id')
                }

        return {
            'title': None,
            'id': None
        }

    def make_name(self, s):
        name = s.split(' ')
        return {
            'last_name': name[0] if len(name) >= 1 else None,
            'first_name': name[1] if len(name) >= 2 else None,
            'middle_name': name[2] if len(name) >= 3 else None,
            'full_name': s
        }

    def normalizers(self, types):
        fns = []
        for t in types:
            if t == "only_numbers":
                fns.append(self.get_numbers)
            elif t == 'make_status':
                fns.append(self.get_status)
            elif t == 'make_name':
                fns.append(self.make_name)
            elif t == 'make_position':
                fns.append(self.make_position)

        return compose(*fns)

