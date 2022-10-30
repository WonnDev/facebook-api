# -*- coding: utf-8 -*-

import requests
from requests.structures import CaseInsensitiveDict


class Cookie:
    def __init__(self, cookie) -> None:
        self.cookie = cookie
        
    def toString(self) -> str:
        cookie = ''
        for x, y in self.cookie.get_dict().items():
            cookie += '{0}={1};'.format(x, y)
        return cookie
    
    def getOnly(self, name) -> str:
        return self.cookie.get_dict()[name]


        
    
        
class FacebookAPI:
    
    
    def __init__(self, cookie=None, ua='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36') -> None:
        self.cookie = cookie
        self.ua = ua
        self.isLogin = False
        self.getCookie = Cookie(cookie)
      
        
    def two_fa (self, token) -> str:
        url = "http://2fa.live/tok/{0}".format(token)
        
        headers = CaseInsensitiveDict()
        headers["Accept"] = "*/*"
        headers["Accept-Language"] = "vi,en;q=0.9,en-US;q=0.8"
        headers["Connection"] = "keep-alive"
        headers["Cookie"] = "_gcl_au=1.1.286133354.1667099945; _ga=GA1.2.856788222.1667099946; _gid=GA1.2.1191880931.1667099946; _gat_gtag_UA_78777107_1=1"
        headers["Referer"] = "http://2fa.live/"
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24"
        headers["X-Requested-With"] = "XMLHttpRequest"
        
        
        resp = requests.get(url, headers=headers)
        return resp.json()['token']
    def loginMbasic (self, two_fa='', email='', password='') -> bool:
        code = ''
        if len(two_fa) > 1:
            code = self.two_fa(two_fa)
        url = "https://mbasic.facebook.com/"
        
        headers = CaseInsensitiveDict()
        headers["authority"] = "mbasic.facebook.com"
        headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        headers["accept-language"] = "en-US,en;q=0.9"
        headers["sec-fetch-dest"] = "document"
        headers["sec-fetch-mode"] = "navigate"
        headers["sec-fetch-site"] = "none"
        headers["sec-fetch-user"] = "?1"
        headers["upgrade-insecure-requests"] = "1"
        headers["user-agent"] = self.ua
        
        
        resp = requests.get(url, headers=headers)
        
        cookie = resp.cookies
        self.currentCookie = cookie
        self.getCookie.cookie = self.currentCookie
        new = requests.get(url, headers=headers, cookies=cookie)
        
        if '<form method="post" action="' in new.text:
            html = new.text
            urlLogin = 'https://mbasic.facebook.com{0}'.format(
                new.text.split('<form method="post" action="')[1].split('"')[0])
            
            cutParams = lambda name: 'name="{0}" value="'.format(name)
            lsd = html.split(cutParams('lsd'))[1].split('"')[0]
            jazoest = html.split(cutParams('jazoest'))[1].split('"')[0]
            m_ts = html.split(cutParams('m_ts'))[1].split('"')[0]
            li = html.split(cutParams('li'))[1].split('"')[0]
            try_number = html.split(cutParams('try_number'))[1].split('"')[0]
            unrecognized_tries = html.split(cutParams('unrecognized_tries'))[1].split('"')[0]
            bi_xrwh = html.split(cutParams('bi_xrwh'))[1].split('"')[0]
            
            data = {
                    'lsd': lsd,
                    'jazoest': jazoest,
                    'm_ts': m_ts,
                    'li': li,
                    'try_number': try_number,
                    'unrecognized_tries': unrecognized_tries,
                    'email': email,
                    'pass': password,
                    'login': 'Log In',
                    'bi_xrwh': bi_xrwh
                }
            
            login = requests.post(urlLogin, headers=headers, data=data, cookies=cookie)
            html = login.text
            
            if 'checkpoint' in html:
                login.cookies.update(cookie)
                cookie = login.cookies
                
                go = requests.get('https://mbasic.facebook.com/checkpoint/?_rdr',
                                  headers=headers,
                                  cookies=cookie
                                  )
                
                html = go.text 
                cookie = go.cookies
                         
                fb_dtsg = html.split(cutParams('fb_dtsg'))[1].split('"')[0]
                jazoest = html.split(cutParams('jazoest'))[1].split('"')[0]
                nh = html.split(cutParams('nh'))[1].split('"')[0]
                fb_dtsg = html.split(cutParams('fb_dtsg'))[1].split('"')[0]
               
                
                data = {
                       'fb_dtsg': fb_dtsg,
                       'jazoest': jazoest,
                       'checkpoint_data': '',
                       'approvals_code': code,
                       'codes_submitted': 0,
                       'submit[Submit Code]:': 'Gửi mã',
                       'nh': nh,
                       'fb_dtsg': fb_dtsg,
                       'jazoest': jazoest,
                    }
                veri = requests.post('https://mbasic.facebook.com/login/checkpoint/', headers=headers, data=data, cookies=cookie)
                cookie = veri.cookies
        
                data = {
                       'fb_dtsg': fb_dtsg,
                       'jazoest': jazoest,
                       'checkpoint_data': '',
                       'name_action_selected': 'dont_save',
                       'submit[Continue]:': 'Tiếp tục',
                       'nh': nh,
                       'fb_dtsg': fb_dtsg,
                       'jazoest': jazoest,
                    }
                
                veri = requests.post('https://mbasic.facebook.com/login/checkpoint/', headers=headers, data=data, cookies=cookie)
                if 'login/checkpoint' in veri.text:
                    cookie = veri.cookies
                    data = {
                           'fb_dtsg': fb_dtsg,
                           'jazoest': jazoest,
                           'checkpoint_data': '',
                           'submit[Continue]:': 'Tiếp tục',
                           'nh': nh,
                           'fb_dtsg': fb_dtsg,
                           'jazoest': jazoest,
                        }
                    nex = requests.post('https://mbasic.facebook.com/login/checkpoint/', headers=headers, data=data, cookies=cookie)
                    self.html = nex.text
                    self.cookie = nex.cookies
                    cookie = nex.cookies
                    if 'login/checkpoint' in nex.text:
                        data = {
                               'fb_dtsg': fb_dtsg,
                               'jazoest': jazoest,
                               'checkpoint_data': '',
                               'submit[This was me]:': 'Đây là tôi',
                               'nh': nh,
                               'fb_dtsg': fb_dtsg,
                               'jazoest': jazoest,
                            }
                        nex = requests.post('https://mbasic.facebook.com/login/checkpoint/', headers=headers, data=data, cookies=cookie)
                        self.html = nex.text
                        self.cookie = nex.cookies
                        cookie = nex.cookies
                        if 'login/checkpoint' in nex.text:
                            data = {
                                   'fb_dtsg': fb_dtsg,
                                   'jazoest': jazoest,
                                   'checkpoint_data': '',
                                   'name_action_selected': 'dont_save',
                                   'submit[Continue]:': 'Tiếp tục',
                                   'nh': nh,
                                   'fb_dtsg': fb_dtsg,
                                   'jazoest': jazoest,
                                }
                            nex = requests.post('https://mbasic.facebook.com/login/checkpoint/', headers=headers, data=data, cookies=cookie)
                            self.html = nex.text
                            self.cookie = nex.cookies
                            self.isLogin = True
                            return True
            if 'login/save-device/cancel/' in html:
                login.cookies.update(cookie)
                cookie = login.cookies
                veriToken = html.split('login/save-device/cancel/?')[1].split('"')[0]
                urlVeri = 'https://mbasic.facebook.com/login/save-device/cancel/?{0}'.format(veriToken)
                
                cancel = requests.get(urlVeri, headers=headers, cookies=cookie)
                
                data = {
                        'lsd': lsd,
                        'jazoest': jazoest,
                        'uid': '100087462814868',
                        'flow': 'login_no_pin',
                        'next': ''
                    }
                
    
                pin = requests.post('https://mbasic.facebook.com/login/device-based/validate-pin/?refid=8', data=data, headers=headers, cookies=cookie)
                html = pin.text
                lsd = html.split(cutParams('lsd'))[1].split('"')[0]
                jazoest = html.split(cutParams('jazoest'))[1].split('"')[0]
                data = {
                  'lsd': lsd,
                  'jazoest': jazoest,
                  'uid': '100087462814868',
                  'next': 'https://mbasic.facebook.com',
                  'flow': 'login_no_pin',
                  'pass': password
                }
                go = requests.post('https://mbasic.facebook.com/login/device-based/validate-password/?shbl=0', headers=headers, data=data, cookies=cookie)
                self.cookie = cookie
                self.html = go.text
                self.isLogin = True
                return True
            else:
               if '<title>Facebook</title>' in html:
                   self.isLogin = True
                   return True
               
               else:
                   return False
