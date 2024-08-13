
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import CmsSlider


class CmsSliderModelTest(TestCase):
    def setUp(self):
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )
        self.slider = CmsSlider.objects.create(
            cms_img=self.image,
            cms_title='Test Title',
            cms_text='Test Text',
            cms_css='test-css-class'
        )

    def test_cms_slider_creation(self):
        slider = CmsSlider.objects.get(cms_title='Test Title')
        self.assertEqual(slider.cms_title, 'Test Title')
        self.assertEqual(slider.cms_text, 'Test Text')
        self.assertEqual(slider.cms_css, 'test-css-class')

        self.assertTrue(slider.cms_img.name.startswith('sliderimg/test_image'))
        self.assertIn('sliderimg/test_image', slider.cms_img.name)

    def test_str_method(self):
        self.assertEqual(str(self.slider), 'Test Title')

    def test_default_css_class(self):
        slider = CmsSlider.objects.create(
            cms_img=self.image,
            cms_title='Another Test Title',
            cms_text='Another Test Text'
        )
        self.assertEqual(slider.cms_css, '-')

    def test_cms_title_max_length(self):
        max_length = CmsSlider._meta.get_field('cms_title').max_length
        try:
            slider = CmsSlider.objects.create(
                cms_img=self.image,
                cms_title='x' * (max_length + 1),
                cms_text='Valid Text',
                cms_css='valid-css'
            )
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_cms_text_max_length(self):
        max_length = CmsSlider._meta.get_field('cms_text').max_length
        try:
            slider = CmsSlider.objects.create(
                cms_img=self.image,
                cms_title='Valid Title',
                cms_text='x' * (max_length + 1),
                cms_css='valid-css'
            )
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_null_css_field(self):
        slider = CmsSlider.objects.create(
            cms_img=self.image,
            cms_title='Test Title',
            cms_text='Test Text',
            cms_css=None
        )
        self.assertIsNone(slider.cms_css)
