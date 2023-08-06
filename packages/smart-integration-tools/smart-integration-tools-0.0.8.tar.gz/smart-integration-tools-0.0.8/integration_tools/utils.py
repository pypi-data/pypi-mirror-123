import re
import json
import requests
from typing import Any, Optional
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Union, Any, Generator
from urllib.parse import urlparse, parse_qs

from .settings import parse_tools_settings

_, DASHBOARD_URL, _, _ = parse_tools_settings()

UTM_PARAMS = (
    'utm_source',
    'utm_medium',
    'utm_campaign',
    'utm_term',
    'utm_content',
    'utm_referrer',
)

__all__ = (
    'parse_utm',
    'remove_tags',
    'UTM_PARAMS',
    'get_smart_token',
    'check_entities_equal',
    'get_full_integrations',
    'get_integration_info',
    'remove_unacceptable_chars',
    'REGEX_PATTERN_VALUES',
)

REGEX_PATTERN_VALUES = (
    '"',
    "'",
    ';',
    ',',
    '==',
    '!=',
    '=@',
    '!@',
    '>',
    '<',
    '>=',
    '<=',
    '=^',
    '!^',
    '=\^',
    '!\^',
    '=$',
    '!$',
    '=\$',
    '!\$',
    '=~',
    '!~',
    '!=',
    '==',
    '!@',
    '=@',
    '<',
    '>',
    '<=',
    '>=',
    '!~',
    '=~',
    '!^',
    '=^',
    '!\^',
    '=\^',
    '!$',
    '=$',
    '!\$',
    '=\$',
    'undefined',
    '\n',
    '\t',
    '\r',
)


def remove_unacceptable_chars(
    value: Optional[str],
    pattern_values: list = REGEX_PATTERN_VALUES,
    default_value: Optional[str] = 'none',
) -> str:
    pattern = r'|'.join(f'{v}' for v in pattern_values)
    if value is None or value == '':
        return default_value
    value = re.sub(pattern, ' ', str(value)).strip()
    words = value.split()
    return ' '.join(sorted(set(words), key=words.index))


def parse_utm(url: str) -> dict:
    """return utm dict

    Args:
        url (str): site url

    Returns:
        dict: utm dict
    """
    out = {}
    try:
        url_params = parse_qs(urlparse(url.replace('#', '')).query)
        for utm in UTM_PARAMS:
            if utm in url_params:
                out[utm] = url_params[utm][0]
        return out
    except (KeyError, ValueError, IndexError, TypeError):
        return {}


def remove_tags(text: str) -> str:
    """remove html tags

    Args:
        text (str): default text

    Returns:
        str: cleared text
    """
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)


def get_smart_token(platform: str, token: str) -> str:
    """Get smart token from dashboard app

    Args:
        platform (str): prod or dev
        token (str): execute token for dash app

    Returns:
        str: Token
    """
    url = f'{DASHBOARD_URL}api/smart_tokens/?platform_id={platform}'
    try:
        r = requests.get(url, headers={"executetoken": token}).json()
    except (requests.ConnectionError, json.JSONDecodeError):
        return 'error'
    return r['token']


def get_full_integrations(platform: str, service_code: str, token: str) -> list:
    """Get integrations from smart by service doe

    Args:
        platform (str): like prod or dev
        service_code (str): like direct
        token (str): execute token

    Returns:
        list: result
    """
    token = get_smart_token(platform, token)
    url = f'{DASHBOARD_URL}api/get_config_url/'
    dash_response = requests.get(f'{url}?platform_id={platform}').json()
    headers = {"Authorization": token}

    config_url = f'{dash_response["config_url"]}?type__code={service_code}&all=1'
    # print(config_url)

    configs = requests.get(config_url, headers=headers).json()
    results = configs["results"]
    while configs["next"]:
        configs = requests.get(configs["next"], headers=headers).json()
        results.extend(configs["results"])
    return results


def check_entities_equal(
    first_entity: Any,
    second_entity: Any,
    exclude_fields: Union[list, tuple] = (
        '_state',
        'date_time',
        'sc_date_time',
        'funnel_stage_duration',
        'id',
    ),
) -> bool:
    """Check to entities equald

    Args:
        first_entity (any): 1st entity
        second_entity (any): 2nd entity
        exclude_fields (Union[list, tuple, None], optional): exclude entities fields. Defaults to (
            '_state',
            'date_time',
            'sc_date_time',
            'funnel_stage_duration',
            'id',
        ).

    Returns:
        bool: True if equals else False
    """
    first_entity = first_entity.__dict__
    second_entity = second_entity.__dict__
    return all(
        (field, second_entity[field]) in first_entity.items()
        for field in first_entity
        if field not in exclude_fields
    )


def dates_chunker(
    date_from: datetime, date_to: datetime, default_delta: int = 4
) -> Generator:
    """Return dataes chunker like [[date1, date2]]

    Args:
        date_from (datetime): from date
        date_to (datetime): to date
        default_delta (int, optional): date range. Defaults to 4.

    Yields:
        Generator: dates generator
    """
    dates_delta = (date_to - date_from).days
    for count in range(0, dates_delta + 1, default_delta):
        if count + default_delta > dates_delta:
            default_delta = dates_delta - count + 1
        yield [
            date_from,
            (date_from + timedelta(days=default_delta - 1)),
        ]
        date_from = date_from + timedelta(days=default_delta)


def get_operations(data: dict) -> dict:
    """create valid calculation dict

    Args:
        data (dict): smart calc value

    Returns:
        dict: parsed cal value
    """
    if data:
        if "cogs" in data or "crm_net_cost" in data:
            data["first_cost"] = (
                data.pop('cogs') if "cogs" in data else data.pop('crm_net_cost')
            )
        if "revenue" in data or "crm_deal_cost" in data:
            data['transaction_amount'] = (
                data.pop('revenue') if "revenue" in data else data.pop('crm_deal_cost')
            )
        return {
            field: str(data[field]).replace('{', '').replace('}', '')
            for field in data
            if data[field]
        }
    return {}


def _calc(calc_str) -> str:
    """calculate

    Args:
        calc_str (str): (value like ('(1 * 2) / 3'))

    Returns:
        str: return calculated value
    """
    val = calc_str.group()
    if not val.strip():
        return val
    return "%s" % eval(val.strip(), {'__builtins__': None})


def calculate(calc_str: str) -> str:
    """return calculated value

    Args:
        calc_str (str): calc stirng

    Returns:
        str: result
    """
    return str(re.sub(r"([0-9\ \.\+\*\-\/(\)]+)", _calc, calc_str))


def replacer(string: str, name: str, value: Any) -> str:
    """replacer

    Args:
        string (str): replace string
        name (str): param name
        value (Any): value

    Returns:
        str: [description]
    """
    string = string.replace(name, Decimal(value).__str__())
    return string


def get_integration_info(
    platform: str, integration_id: int, token: Optional[str] = None
) -> dict:
    if not token:
        token = get_smart_token(platform)
    config_url = f'{DASHBOARD_URL}api/get_config_url/?platform_id={platform}'
    dash_response = requests.get(f'{config_url}').json()
    headers = {"Authorization": token}
    integration_url = f'{dash_response["config_url"]}{integration_id}/'
    integration = requests.get(integration_url, headers=headers).json()
    return integration
