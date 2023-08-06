## tools for integrations

### install
Install using `pip`...

    pip install smart-integration-tools


### usage
```python
# in your settings/config file
from integration_tools.settings import init_tools_settings
init_tools_settings(s3_bucket_name='<s3_bucket_name>', dashboard_url='<dashboard_url>')
```

### tools
```python
from integration_tool.chunk import chunk_of_generators, chunk_by_items, chunk_by_parts

list_ = [i for i in range(1, 100000000)]
chunk_of_generators(iter(list_), 25000) # split your iterator/generator for 25000 items

data = [i for i in range(1, 100000000)]
chunk_by_items(data, 10000) # return generator for split your list by 10000

data = [i for i in range(1, 100000000)]
chunk_by_parts(data, 5) # return generator for split your list by 5 pars

from integration_tools.file import delete_file

delete_file('<path to file>') # delete file from your disc

from integration_tools.file import write_csv_file

data = [{str(i): i} for i in range(1, 100000000)]
 # write tsv/csv file
write_csv_file(filename='<path_to_file>', date=data, fieldsnames = None, delimiter='\t', extension='.tsv')

# s3.py

from integration_tools.s3 import upload_to_s3

upload_to_s3(filename='<path_to_local_file>', folder='stats/') # filename - local file, folder - folder on s3 bucket

from integration_tools.s3 import get_s3_file_link, delete_s3_file, check_s3_file_exist, upload_to_s3_from_ram

get_s3_file_link(filename='filename', folder='stats/', extension='.tsv') # get link to download file(not download from boto3)

delete_s3_file(filename='<filename>', folder='stats/', extension='.tsv') # delete file from s3 bucket

check_s3_file_exist(filename='<filename>', folder='stats/') # return True if file exist

from io import StringIO
f = StringIO()
upload_to_s3_from_ram(context=f, filename='<filename>', folder='stats/', extension='.tsv')
f.close()

# crypt.py
from integration_tools.crypt import encrypt, decrypt

credential_secure_password = '1qazxsw2'
token = '<token>'
encoded = encrypt(credential_secure_password, token) # encrypt secure data
decoded = decrypt(encoded, token) # decrypt secure data

# decrypt data
from integration_tools.crypt import decrypt_data

# your view
data = request.data
access_token = 'access_token'
secret_token = 'secret_token'
decrypted_data = decrypt_data(data, '<secret_token>', secret_token)

#filters.py
from integration_tools.filters import validate_data, parse_for_django_query, parse_for_mongo_query
filter_str = "url=@test.ru;!url=@google;!url=@yandex;!url=@yahoo"

## for filter you must be compare validate_obj(dict)
## check filter
validated_obj = {'url': 'test.ru/123', 'entity_id':1, 'entity_name': 'test_obj'}
validate_data(filter_str, validated_obj) # return True

# parse for orms
filter_str = "url=@test.ru,!url=@google"
parse_for_django_query(filter_str) # return [{'filter': {'url__iexact': 'test.ru'}, 'exclude': {}}, {'filter': {}, 'exclude': {'url__iexact': 'google'}}]
parse_for_mongo_query(filter_str) # return [{'url__regex': 'test.ru'}, {'url__regex_ne': 'google'}]

# utils.py
from integration_tools.utils import parse_utm, remove_tags, get_smart_token, check_entities_equal, get_full_integrations

url = 'https://test.io/?utm_source=google&utm_medium=cpc&utm_campaign=1'
utm = parse_utm(url) # return {'utm_source': 'google', 'utm_medium': 'cpc', 'utm_campaign': '1'}

integrations = get_full_integrations('prod', 'yandex_direct', '<execute_token>') # return list of integrations by code

token = get_smart_token('prod', '<execute_token>') # return Smart Access token

from copy import deepcopy
from integration_utils.tools import check_entities_equal
from .models import Deal
db_deal = Deal.objects.first()
new_deal = deepcopy(db_deal)
new_deal.name = '123'

check_entities_equal(first_entity=db_deal, second_entity=new_deal) # return True/False check to deals equals

without_html_tags = remove_tags('<string_with_html_tags>')

```