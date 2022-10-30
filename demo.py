# -*- coding: utf-8 -*-


import facebook_api



# login fb
obj = facebook_api.FacebookAPI()
if obj.loginMbasic(
    email='taikhaon...@gmail.com', password='depchai', two_fa='kocaigi'
    ) == True:
    print('Dang nhap thanh cong')
    print(obj.getCookie.toString())
