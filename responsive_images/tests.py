from django.test import TestCase
from django.conf import settings
from django.contrib.staticfiles import finders

from .utils import get_resized_image, get_final_resolution, get_file

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

    def test_get_final_resolution(self):
        old_resolutions = getattr(
            settings, 'RESPONSIVE_IMAGE_RESOLUTIONS', None)
        new_resolutions = [
            1382, 1068, 992, 850, 800, 768, 700, 600, 480, 350,
            250, 150, 80, 40]
        setattr(settings, 'RESPONSIVE_IMAGE_RESOLUTIONS', new_resolutions)
        cookies = {'resolution': 1400}
        self.assertEqual(1382, get_final_resolution(cookies))
        cookies = {'resolution': 1200}
        self.assertEqual(1068, get_final_resolution(cookies))
        cookies = {'resolution': 1000}
        self.assertEqual(992, get_final_resolution(cookies))
        cookies = {'resolution': 770}
        self.assertEqual(768, get_final_resolution(cookies))
        cookies = {'resolution': 60}
        self.assertEqual(40, get_final_resolution(cookies))
        cookies = {'resolution': 40}
        self.assertEqual(40, get_final_resolution(cookies))
        cookies = {'resolution': 20}
        self.assertEqual(40, get_final_resolution(cookies))
        self.assertEqual(100, get_final_resolution({}))
        if old_resolutions:
            settings.RESPONSIVE_IMAGE_RESOLUTIONS = old_resolutions
        else:
            delattr(settings, 'RESPONSIVE_IMAGE_RESOLUTIONS')

    def test_get_final_resolution_optional_setting(self):
        old_resolutions = None
        if hasattr(settings, 'RESPONSIVE_IMAGE_RESOLUTIONS'):
            old_resolutions = settings.RESPONSIVE_IMAGE_RESOLUTIONS
            delattr(settings, 'RESPONSIVE_IMAGE_RESOLUTIONS')
        cookies = {'resolution': 480}
        self.assertEqual(480, get_final_resolution(cookies))
        if old_resolutions:
            setattr(settings, 'RESPONSIVE_IMAGE_RESOLUTIONS', old_resolutions)

    def test_get_file(self):
        test_image = settings.RESPONSIVE_IMAGE_FOR_TEST
        extension = test_image.split(".").pop()
        image_full_path = finders.find(test_image)
        response = get_file(image_full_path, extension)
        response_content = response.content
        file_content = open(image_full_path).read()
        self.assertEqual(response_content, file_content)
