from contextlib import suppress
from json import JSONDecodeError, loads
from typing import Dict, Tuple, Union, Any

import requests
from bs4 import BeautifulSoup

from .errors import *
from .utils import AttrDict


class Client:
    def __init__(self, token: str, host: str = 'https://sms-activate.ru/stubs/handler_api.php') -> None:
        self._host = f'{host}?api_key={token}'
        self._session = requests.Session()
        self._token = token

    def _make_request(self, path: str, method: str = 'post',
                      **kwargs: Dict[Any, Any]) -> Tuple[Union[Dict, str], Response]:
        req = self._session.request(method, f'{self._host}/{path}',
                                    **kwargs)

        resp = req.text

        if 'NO_NUMBERS' in resp:
            raise NO_NUMBERS()
        elif 'NO_BALANCE' in resp:
            raise NO_BALANCE()
        elif 'BAD_ACTION' in resp:
            raise BAD_ACTION()
        elif 'BAD_SERVICE' in resp:
            raise BAD_SERVICE()
        elif 'BAD_KEY' in resp:
            raise BAD_KEY()
        elif 'ERROR_SQL' in resp:
            raise ERROR_SQL()
        elif 'SQL_ERROR' in resp:
            raise SQL_ERROR()
        elif 'NO_ACTIVATION' in resp:
            raise NO_ACTIVATION()
        elif 'BAD_STATUS' in resp:
            raise BAD_STATUS()
        elif 'STATUS_CANCEL' in resp:
            raise STATUS_CANCEL()
        elif 'BANNED' in resp:
            raise BANNED()
        elif 'NO_CONNECTION' in resp:
            raise NO_CONNECTION()
        elif 'ACCOUNT_INACTIVE' in resp:
            raise ACCOUNT_INACTIVE()
        elif 'NO_ID_RENT' in resp:
            raise NO_ID_RENT()
        elif 'INVALID_PHONE' in resp:
            raise INVALID_PHONE()
        elif 'STATUS_FINISH' in resp:
            raise STATUS_FINISH()
        elif 'STATUS_WAIT_CODE' in resp:
            raise STATUS_WAIT_CODE()
        elif 'INCORECT_STATUS' in resp:
            raise INCORECT_STATUS()
        elif 'CANT_CANCEL' in resp:
            raise CANT_CANCEL()
        elif 'ALREADY_FINISH' in resp:
            raise ALREADY_FINISH()
        elif 'ALREADY_CANCEL' in resp:
            raise ALREADY_CANCEL()
        elif ':' not in resp:
            raise Error(req)

        try:
            return AttrDict(req.json()), req
        except JSONDecodeError:
            req_text = req.text.split(':')
            req_text.remove(req_text[0])
            req_text = ':'.join(req_text)

            try:
                return AttrDict(loads(req_text)), req
            except (JSONDecodeError, TypeError):
                return req_text, req

    def get_numbers_status(self, country: int = None, operator: str = None) -> dict[str, int]:
        params = {
            'action': 'getNumbersStatus'
        }

        if country:
            params['country'] = country

        if operator:
            params['operator'] = operator

        resp, _ = self._make_request('', **{'data': params})

        return resp

    def get_balance(self) -> float:
        params = {
            'action': 'getBalance'
        }

        resp, _ = self._make_request('', **{'data': params})

        return float(resp)

    def get_balance_cashback(self) -> float:
        params = {
            'action': 'getBalanceAndCashBack'
        }

        resp, _ = self._make_request('', **{'data': params})

        return float(resp)

    def get_number(self, service: str, country: int = None, forward: int = 0, operator: str = None, ref: str = None):
        params = {
            'action': 'getNumber',
            'service': service,
            'forward': forward
        }

        if country:
            params['country'] = country

        if operator:
            params['operator'] = operator

        if ref:
            params['ref'] = ref

        resp, _ = self._make_request('', **{'data': params})

        return resp

    def set_status(self, id: int, status: int, forward: int = 0):
        params = {
            'action': 'setStatus',
            'id': id,
            'status': status
        }

        if forward:
            params['forward'] = forward

        resp, _ = self._make_request('', **{'data': params})

        return resp

    def get_status(self, id: int):
        params = {
            'action': 'getStatus',
            'id': id
        }

        resp, _ = self._make_request('', **{'data': params})

        return resp

    def get_full_sms(self, id: int):
        params = {
            'action': 'getFullSms',
            'id': id
        }

        resp, _ = self._make_request('', **{'data': params})

        return resp

    def get_prices(self, country: int = None, service: str = None) -> dict:
        params = {
            'action': 'getPrices'
        }

        if country:
            params['country'] = country

        if service:
            params['service'] = service

        resp, _ = self._make_request('', **{'data': params})

        return resp

    def get_best_price(self, service: str = None) -> dict:
        tg_services = self.get_prices(service=service)
        best_service = {'0': 9999999999}

        for country_id in tg_services:
            best_service_cost = list(best_service.values())[0]
            with suppress(AttributeError):
                service_cost = tg_services[country_id].get(service).get('cost')
                service_count = tg_services[country_id].get(service).get('count')

            if service_count and service_cost < best_service_cost:
                best_service = {country_id: service_cost}

        return best_service

    def get_all_countries(self) -> dict:
        params = {
            'action': 'getCountries'
        }

        resp, _ = self._make_request('', **{'data': params})

        return resp

    def get_qiwi_requisites(self):
        params = {
            'action': 'getQiwiRequisites'
        }

        resp, _ = self._make_request('', **{'data': params})

        return resp

    def get_rent_services_and_countries(self, time: int = 1, operator: str = 'any'):
        params = {
            'action': 'getRentServicesAndCountries',
            'time': time,
            'operator': operator
        }

        resp, _ = self._make_request('', **{'data': params})

        return resp

    def get_additional_service(self, service: str, id: int):
        params = {
            'action': 'getAdditionalService',
            'service': service,
            'id': id
        }

        resp, _ = self._make_request('', **{'data': params})

        return resp

    def get_rent_number(self, service: str, time: int = 1, country: int = 0, operator: str = 'any', url: str = ''):
        params = {
            'action': 'getRentNumber',
            'time': time,
            'service': service,
            'rent_time': time,
            'operator': operator,
            'country': country,
            'url': url
        }

        resp, _ = self._make_request('', **{'data': params})

        return resp

    def get_rent_status(self, id: int):
        params = {
            'action': 'getRentStatus',
            'id': id
        }

        resp, _ = self._make_request('', **{'data': params})

        return resp

    def set_rent_status(self, id: int, status: int):
        params = {
            'action': 'setRentStatus',
            'id': id,
            'status': status
        }

        resp, _ = self._make_request('', **{'data': params})

        return resp

    def get_countries(self) -> list:
        response = requests.get('https://sms-activate.ru/en/api2#additionalService').text
        soup = BeautifulSoup(response, 'lxml')

        table = soup.find('table', attrs={'id': 'tableListCountries'})
        table_body = table.find('tbody')

        data = []

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            cols = [ele for ele in cols if ele]
            data.append((cols[0], cols[1]))

        return data

    def get_services(self) -> list:
        response = requests.get('https://sms-activate.ru/en/api2#additionalService').text
        soup = BeautifulSoup(response, 'lxml')

        table = soup.find('table', attrs={'id': 'tableListServices'})
        table_body = table.find('tbody')

        data = []

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            cols = [ele for ele in cols if ele]
            data.append((cols[0], cols[1]))

        return data

    def get_operators(self) -> list:
        response = requests.get('https://sms-activate.ru/en/api2#additionalService').text
        soup = BeautifulSoup(response, 'lxml')

        table = soup.find('table', attrs={'id': 'tableListOperators'})
        table_body = table.find('tbody')

        data = []

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            cols = [ele for ele in cols if ele]
            data.append((cols[0], cols[1], cols[2].replace('&nbsp', '').split(',')))

        return data
