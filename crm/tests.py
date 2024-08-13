from django.test import TestCase, Client
from .models import StatusCrm, Order, ComentCrm
from django.urls import reverse
from .models import Order
from cms.models import CmsSlider
from price.models import PriceCard, PriceTable
from django.contrib.auth import get_user_model
from unittest.mock import patch
class StatusCrmTestCase(TestCase):
    def setUp(self):
        self.status = StatusCrm.objects.create(status_name='Active')

    def test_status_creation(self):
        self.assertEqual(self.status.status_name, 'Active')

    def test_str_method(self):
        self.assertEqual(str(self.status), 'Active')

class OrderTestCase(TestCase):
    def setUp(self):
        self.status = StatusCrm.objects.create(status_name='Active')
        self.order = Order.objects.create(
            order_name='John Doe',
            order_phone='123456789',
            order_status=self.status
        )

    def test_order_creation(self):
        self.assertEqual(self.order.order_name, 'John Doe')
        self.assertEqual(self.order.order_phone, '123456789')
        self.assertEqual(self.order.order_status, self.status)

    def test_str_method(self):
        self.assertEqual(str(self.order), 'John Doe')

class ComentCrmTestCase(TestCase):
    def setUp(self):
        self.status = StatusCrm.objects.create(status_name='Active')
        self.order = Order.objects.create(
            order_name='John Doe',
            order_phone='123456789',
            order_status=self.status
        )
        self.coment = ComentCrm.objects.create(
            coment_binding=self.order,
            coment_text='This is a comment'
        )

    def test_coment_creation(self):
        self.assertEqual(self.coment.coment_text, 'This is a comment')
        self.assertEqual(self.coment.coment_binding, self.order)

    def test_str_method(self):
        self.assertEqual(str(self.coment), 'This is a comment')


class ViewTests(TestCase):

    def setUp(self):
        self.slider1 = CmsSlider.objects.create(
            cms_title='первый слайд',
            cms_img='sliderimg/1.jpg'
        )
        self.slider2 = CmsSlider.objects.create(
            cms_title='второй слайд',
            cms_img='sliderimg/2.jpg'
        )

        self.pc1 = PriceCard.objects.create(
            pc_value='100',
            pc_description='Price Card 1'
        )
        self.pc2 = PriceCard.objects.create(
            pc_value='200',
            pc_description='Price Card 2'
        )
        self.pc3 = PriceCard.objects.create(
            pc_value='300',
            pc_description='Price Card 3'
        )

        self.price_table = PriceTable.objects.create(
            pt_title='Price Table 1',
            pt_old_price='150',
            pt_new_price='100'
        )
    def test_first_page_view(self):
        response = self.client.get(reverse('first_page'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('slider_list', response.context)
        self.assertIn('pc_1', response.context)
        self.assertIn('pc_2', response.context)
        self.assertIn('pc_3', response.context)
        self.assertIn('price_table', response.context)
        self.assertIn('form', response.context)



def test_thanks_page_view_get(self):
        response = self.client.get(reverse('thanks_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thanks.html')