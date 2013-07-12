from django.test import TestCase
from django.conf import settings
from django.contrib.staticfiles import finders

from .utils import get_resized_image

from PIL import Image

import os


class TestUtils(TestCase):
    def test_get_resized_image(self):
        test_image = settings.RESPONSIVE_IMAGE_FOR_TEST
        full_path = finders.find(test_image)
        i = Image.open(full_path)
        final_resolution = i.size[0]/4
        resized_image_full_path = get_resized_image(
            test_image, final_resolution)[0]
        resized_image = Image.open(resized_image_full_path)
        aspect_ratio = i.size[1]/float(i.size[0])
        required_final_width = final_resolution
        required_final_height = int(final_resolution * aspect_ratio)
        self.assertEqual(required_final_width, resized_image.size[0])
        self.assertEqual(required_final_height, resized_image.size[1])
        os.remove(resized_image_full_path)

    def test_get_resized_image_bigger_resolution(self):
        test_image = settings.RESPONSIVE_IMAGE_FOR_TEST
        full_path = finders.find(test_image)
        i = Image.open(full_path)
        final_resolution = i.size[0]*2
        resized_image_full_path = get_resized_image(
            test_image, final_resolution)[0]
        resized_image = Image.open(resized_image_full_path)
        self.assertEqual(i.size[0], resized_image.size[0])
        self.assertEqual(i.size[1], resized_image.size[1])

    def test_get_resized_image_new_cache_dir(self):
        old_cache_dir_name = getattr(
            'settings', 'RESPONSIVE_IMAGES_CACHE_DIR',
            'responsive_images_cache')
        new_cache_dir_name = 'abcdefgh56894735jkhsdfjk'
        settings.RESPONSIVE_IMAGES_CACHE_DIR = new_cache_dir_name
        test_image = settings.RESPONSIVE_IMAGE_FOR_TEST
        full_path = finders.find(test_image)
        i = Image.open(full_path)
        final_resolution = i.size[0]/4
        resized_image_full_path = get_resized_image(
            test_image, final_resolution)[0]
        resized_image = Image.open(resized_image_full_path)
        aspect_ratio = i.size[1]/float(i.size[0])
        required_final_width = final_resolution
        required_final_height = int(final_resolution * aspect_ratio)
        self.assertEqual(required_final_width, resized_image.size[0])
        self.assertEqual(required_final_height, resized_image.size[1])
        os.remove(resized_image_full_path)
        if hasattr(settings, 'RESPONSIVE_IMAGES_CACHE_DIR'):
            settings.RESPONSIVE_IMAGES_CACHE_DIR = old_cache_dir_name
        os.removedirs(finders.find(new_cache_dir_name))
