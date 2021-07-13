import random, string, requests, base64
from time import sleep
from requests.exceptions import ConnectTimeout

BASE_PREFIX = str(base64.b64decode('aHR0cHM6Ly9kZWVwbnVkZS50bw==').decode('utf-8'))
TOKLEN_SESSIONID = 32
TOKLEN_IMGID = 15

class url_prefixes():
    status = '/api/status/'
    upload_request = '/api/request-upload/'
    image_upload = '/upload/'
    get_im_prefix = '/img/'
    get_im_suffix = '/watermark.jpg'

def generate_random_token(toklen):
    token = ''.join(random.choices(string.ascii_lowercase + string.digits, k = toklen))
    return token

def check_ping():
    try:
        r=requests.get(url=BASE_PREFIX+ url_prefixes.status, timeout=(25, 30)).status_code
    except ConnectTimeout:
        r = 408
    return r
    
def get_upload_perm(image_id, cookie):
    headers = {
    'Host': BASE_PREFIX.split('/')[2],
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': '{}'.format(BASE_PREFIX),
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': '{}'.format(BASE_PREFIX),
    'Cookie': 'userid={0}; identifier={0}'.format(cookie),
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'Trailers',
    }
    url = BASE_PREFIX + url_prefixes.upload_request + image_id
    r = requests.post(url=url, headers=headers)
    return r.content.decode('utf-8')

def upload_image(image_id, cookie, filename):
    data = open(filename, 'rb').read()
    headers = {
    'Host': BASE_PREFIX.split('/')[2],
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'image/jpeg',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length':'{0}'.format(str(len(data)-3)),
    'Origin': '{}'.format(BASE_PREFIX),
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': '{}'.format(BASE_PREFIX),
    'Cookie': 'userid={0}; identifier={0}'.format(cookie),
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'Trailers',
    }
    url = BASE_PREFIX + url_prefixes.image_upload + image_id
    r = requests.put(url=url, headers=headers, data=data)
    return r.status_code

def get_image(image_id, cookie):
    sleep(20)
    headers={
    'Host': BASE_PREFIX.split('/')[2],
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Accept': 'image/webp,*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': '{}'.format(BASE_PREFIX),
    'Cookie': 'userid={0}; identifier={0}'.format(cookie),
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'Trailers',
    }
    url = BASE_PREFIX + url_prefixes.get_im_prefix + image_id + url_prefixes.get_im_suffix
    rs = requests.get(url=url, headers=headers)
    return rs.status_code, rs.content
