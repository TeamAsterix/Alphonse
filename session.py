from pyrogram import Client

 lang = input('Select lang (en): ').lower()

 if lang == 'en':
     print('''\nPlease go to my.telegram.org
 Login using your Telegram account
 Click on API Development Tools
 Create a new application, by entering the required details\n''')

     API_ID = ''
     API_HASH = ''

     while not API_ID.isdigit() or len(API_ID) < 5 or len(API_ID) > 7:
         API_ID = input('API ID: ')

     API_ID = int(API_ID)

     while len(API_HASH) != 32:
         API_HASH = input('API HASH: ')

     app = Client(
         'alphonseuserbot',
         api_id=API_ID,
         api_hash=API_HASH,
         app_version='AlphonseEcem',
         device_model='Firefox 91.0.2',
         system_version='Session',
         lang_code='en',
     )

     with app:
         self = app.get_me()
         session = app.export_session_string()
         out = f'''**Hi [{self.first_name}](tg://user?id={self.id})
 \nAPI_ID:** `{API_ID}`
 \n**API_HASH:** `{API_HASH}`
 \n**SESSION:** `{session}`
 \n**NOTE: Don't give your account information to others!**'''
         out2 = 'Session successfully generated!'
         if self.is_bot:
             print(f'{session}\n{out2}')
         else:
             app.send_message('me', out)
             print('''Session successfully generated!
 Please check your Telegram Saved Messages''')


 