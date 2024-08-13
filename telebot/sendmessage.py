import requests
from .models import TeleSettings

def format_message(text, tg_name, tg_phone):
    if not text:
        raise ValueError("Message text is None or empty")
    if not tg_name or not tg_phone:
        raise ValueError("Name or phone is None or empty")
    if '{' in text and '}' in text:
        part_1 = text.split('{')[0]
        part_2 = text.split('}')[1].split('{')[0]
        part_3 = text.split('}')[-1]
        return part_1 + tg_name + part_2 + tg_phone + part_3
    return text

def sendTelegram(tg_name, tg_phone):
    try:
        settings = TeleSettings.objects.get(pk=1)
    except TeleSettings.DoesNotExist:
        return 'TeleSettings object does not exist'

    token = str(settings.tg_token)
    chat_id = str(settings.tg_chat)
    text = str(settings.tg_message)
    api = 'https://api.telegram.org/bot'
    method = api + token + '/sendMessage'

    text_slice = format_message(text, tg_name, tg_phone)

    try:
        response = requests.post(method, data={
            'chat_id': chat_id,
            'text': text_slice
        })
        response.raise_for_status()
    except requests.HTTPError as http_err:
        return f'HTTP error occurred: {http_err}'
    except Exception as err:
        return f'Other error occurred: {err}'
    else:
        return 'Всё Ок сообщение отправлено!'
