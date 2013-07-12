from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.contrib.staticfiles import finders
from django.http import HttpResponse


from PIL import Image

import os


def get_final_resolution(cookies):
    resolution = None
    try:
        resolution = int(cookies['resolution'])
    except KeyError:
        return 100
    try:
        resolutions = settings.RESPONSIVE_IMAGE_RESOLUTIONS
    except AttributeError:
        resolutions = [1382, 992, 768, 480]
    resolutions.sort()
    resolutions.reverse()
    final_resolution = resolutions[0]
    if resolution < resolutions[0]:
        for r in resolutions:
            if resolution > r:
                final_resolution = r
                break
    if resolution <= resolutions[-1]:
        final_resolution = resolutions[-1]
    return final_resolution


def get_file(filename_with_path, extension):
    f = file(filename_with_path, "rb")
    wrapper = FileWrapper(f)
    if extension not in ['png', 'jpg', 'jpeg', 'gif']:
        mimetype = 'image/jpeg'
    else:
        mimetype = 'image/%s' % extension
    response = HttpResponse(wrapper, mimetype=mimetype)
    response['Content-Length'] = os.path.getsize(filename_with_path)
    response['Content-Disposition'] = \
        'attachment; filename={0}'.format(filename_with_path.split("/").pop())
    return response

def get_resized_image(filename, final_resolution):
    fullname = finders.find(filename)
    filename = filename.split("/").pop()
    filename, extension = filename.split(".")
    i = Image.open(fullname)
    aspect_ratio = i.size[1]/float(i.size[0])
    final_width = final_resolution
    final_height = int(final_resolution*aspect_ratio)

    if i.size[0] < final_resolution:
        return fullname, extension
    filename = "%s_%s_%s.%s" % (filename, final_width, final_height,
                             extension)

    cache_dir_name = getattr(settings, 'RESPONSIVE_IMAGES_CACHE_DIR',
                             'responsive_images_cache')
    cache_path = os.path.join(settings.MEDIA_ROOT, cache_dir_name)
    if not finders.find(cache_dir_name):
        os.mkdir(cache_path)

    resized_image_full_path = os.path.join(cache_path, filename)

    if not finders.find(cache_dir_name + "/" + filename):
        size = (final_width, final_height)
        resized_image = i.resize(size, Image.ANTIALIAS)
        resized_image.save(resized_image_full_path, extension,
            quality=getattr('settings', cache_dir_name, 75)) 
    return resized_image_full_path, extension
