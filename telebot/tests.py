from unittest.mock import patch, Mock
from django.test import TestCase
from .models import TeleSettings
from .sendmessage import sendTelegram
import requests
class SendTelegramTestCase(TestCase):

    def setUp(self):
        TeleSettings.objects.create(
            tg_token='7007754749:AAHZlTIGflUWPdUvMt_HB7lUt80tmPARcQE',
            tg_chat='-4247438980',
            tg_message='Привет {name}, твой телефон {phone}?'
        )

    @patch('requests.post')
    def test_send_telegram_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        result = sendTelegram('Тест Тест', '+9999999999')
        self.assertEqual(result, 'Всё Ок сообщение отправлено!')
        mock_post.assert_called_once_with(
            'https://api.telegram.org/bot7007754749:AAHZlTIGflUWPdUvMt_HB7lUt80tmPARcQE/sendMessage',
            data={
                'chat_id': '-4247438980',
                'text': 'Привет Тест Тест, твой телефон +9999999999?'
            }
        )

    @patch('requests.post')
    def test_send_telegram_failure(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.HTTPError('HTTP error')
        mock_post.return_value = mock_response

        result = sendTelegram('Тест Тест', '+9999999999')
        # print("Result:", result)
        self.assertIn('HTTP error occurred', result)
    @patch('requests.post')
    def test_send_telegram_exception(self, mock_post):
        mock_post.side_effect = Exception('Connection error')

        result = sendTelegram('Тест Тест', '+9999999999')
        self.assertIn('Other error occurred', result)
