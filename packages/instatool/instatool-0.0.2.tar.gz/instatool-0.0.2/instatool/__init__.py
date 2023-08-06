import requests

s = requests.session()
login_Headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'content-length': '318',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'mid=YSma9gALAAHwbHKIhuux1KzBdiZB; ig_did=56438543-E7CE-4F94-BF2F-775E3EFF14A5; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; shbid="11806\05446630507089\0541665950374:01f7ba3214773a068855d3127d477b577f1d65ee7700c3dea4a54f2cebb5417067c6fce6"; shbts="1634414374\05446630507089\0541665950374:01f70d00fd5524f918666abd31eae55de19df3e0c0fc6634e692c44ba0cb62e84dde2a40"; csrftoken=p9lrKwGNFBtZGPlazVEzhyNaewxxZeDS; fbsr_124024574287414=tQs_sqNzLEYWXBcgYFHahtra3ZuS8CNz-L-O-Hi2o9Q.eyJ1c2VyX2lkIjoiMTAwMDAyNzMwODc3MjYyIiwiY29kZSI6IkFRQTFHTWJ0RGVqeFhPRDFsbVptSURFR09PTG9wNTQzMHhVMWZJTFRqTjhPbnZuRDJVRzdNY1ZFQUhhSFNCUUN0R3NYaDNrdVl6QTFUbWtRWEotdXI2NWdOd3Y0RlYxVWs1VlBFS0lNV2FQcWRpNm40dkJkMERCbGZwaXBTbTZYMEJMUUxwcTJMRlF5TkZhR0NxM2MxQkRlOFFaZXdjZXQ2NTRNZVJOTjVCTEVqRXJWUTRqd3Q3OURTR1FMUURDLXVJWXoxNmxIclphRklwUUVhT2U4a2ZFc0VrWmFjeHBhTjJoZGFEVWRxYVJHUzNtNmRGUTRaNjNCNjRHS2Zuam4xYk1YeEQtVmVHN0dLa0gzLVBhaTFlc3JsQUZjQzZISldNNkczUjB0Y0FYR3RHdXpRUFREYndZWDdoR04xWkdMZTVubDVFRjdJQXJLRnhxTjNobW9wZldGIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUlmRVFyY2NGTzA5UUlqM2g2T1pCcTVHZnJudnR0UzZFZVVwejlNY1ZmUm9aQms3NUN0WkJxMjRXVGxodm5YV01pc2t0dktId2d2QWZrcnRkaTdwWkFRV0tsSXJYTHQ4dEh2UkxoYm12R2E1SE5zcTRSeXl1MlpBckFKWG9ic0NWTXhCYXFiWWpUZ0JuN1pBV1VoTnJsT1BDWEdhNUJYU2l5SDY5QmJvNXpnZjdxTmx4ekdaQVM4Sk5oaThlUFU5d1pEWkQiLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTYzNDQ3Mzk1NX0',
    'origin': 'https://www.instagram.com',
    'referer': 'https://www.instagram.com/accounts/emailsignup/',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'x-asbd-id': '198387',
    'x-csrftoken': 'p9lrKwGNFBtZGPlazVEzhyNaewxxZeDS',
    'x-ig-app-id': '936619743392459',
    'x-ig-www-claim': '0',
    'x-instagram-ajax': 'fded3d1a393b',
    'x-requested-with': 'XMLHttpRequest',
}

class grab:
    def name(user,cookie):
        Headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        }
        try:
            r = s.get(f'https://www.instagram.com/{user}/?__a=1', headers=Headers).json()
            return (r['graphql']['user']['full_name'])
        except:
            return ("Error account is banded")

    def bio(user,cookie):
        Headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        }
        try:
            r = s.get(f'https://www.instagram.com/{user}/?__a=1', headers=Headers).json()
            return (r['graphql']['user']['biography'])
        except:
            return ("Error account is banded")

    def followers(user,cookie):
        Headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        }
        try:
            r = s.get(f'https://www.instagram.com/{user}/?__a=1', headers=Headers).json()
            return (r['graphql']['user']['edge_followed_by']['count'])
        except:
            return ("Error account is banded")

    def following(user,cookie):
        Headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        }
        try:
            r = s.get(f'https://www.instagram.com/{user}/?__a=1', headers=Headers).json()
            return (r['graphql']['user']['edge_follow']['count'])
        except:
            return ("Error account is banded")

    def posts(user,cookie):
        Headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        }
        try:
            r = s.get(f'https://www.instagram.com/{user}/?__a=1', headers=Headers).json()
            return (r['graphql']['user']['edge_owner_to_timeline_media']['count'])
        except:
            return ("Error account is banded")

    def id(user,cookie):
        Headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        }
        try:
            r = s.get(f'https://www.instagram.com/{user}/?__a=1', headers=Headers).json()
            return (r['graphql']['user']['id'])
        except:
            return ("Error account is banded")

    def is_business_account(user,cookie):
        Headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        }
        try:
            r = s.get(f'https://www.instagram.com/{user}/?__a=1', headers=Headers).json()
            return (r['graphql']['user']['is_business_account'])
        except:
            return ("Error account is banded")

    def is_new_account(user,cookie):
        Headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        }
        try:
            r = s.get(f'https://www.instagram.com/{user}/?__a=1', headers=Headers).json()
            return (r['graphql']['user']['is_joined_recently'])
        except:
            return ("Error account is banded")

    def is_verified(user,cookie):
        Headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        }
        try:
            r = s.get(f'https://www.instagram.com/{user}/?__a=1', headers=Headers).json()
            return (r['graphql']['user']['is_verified'])
        except:
            return ("Error account is banded")

    def is_private(user,cookie):
        Headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        }
        try:
            r = s.get(f'https://www.instagram.com/{user}/?__a=1', headers=Headers).json()
            return (r['graphql']['user']['is_private'])
        except:
            return ("Error account is banded")

    def get_pic(user,cookie):
        Headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        }
        try:
            r = s.get(f'https://www.instagram.com/{user}/?__a=1', headers=Headers).json()
            return (r['graphql']['user']['profile_pic_url_hd'])
        except:
            return ("Error account is banded")

    def login(user,password):
        login_data = {
            'username': user,
            'enc_password': '#PWD_INSTAGRAM_BROWSER:0:&:' + password
        }
        r = requests.post('https://www.instagram.com/accounts/login/ajax/', headers=login_Headers , data=login_data).text
        if ('"authenticated":false') in r:
            return False
        else:
            return True

def coder():
    return {
        'name':'yazan alqasem',
        'telegram':'@Plugin',
        'channel':'https://t.me/CodeLeak'
    }