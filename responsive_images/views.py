from django.conf import settings
from django.contrib.staticfiles import finders

from responsive_images.utils  import get_final_resolution, get_file

from PIL import Image

import os
from subprocess import call


def adapt_image(request):
    try:
        resolution = int(request.COOKIES['resolution'])
        final_resolution = get_final_resolution(resolution)
    except KeyError:
        final_resolution = 100

    filename = request.META['QUERY_STRING'].replace(settings.IMAGE_ENDS_WITH, "")

    if filename.find(settings.STATIC_URL) == 0:
        filename = filename[len(settings.STATIC_URL):]
    elif filename.find(settings.MEDIA_URL) == 0:
        filename = filename[len(settings.MEDIA_URL):]
    else:
        return None
    
    fullname = finders.find(filename)
    filename = filename.split("/").pop()
    filename, extension = filename.split(".")
    i = Image.open(fullname)
    aspect_ratio = i.size[1]/float(i.size[0])
    final_width = final_resolution
    final_height = int(final_resolution*aspect_ratio)

    if max(i.size[0], i.size[1]) < final_resolution:
        return get_file(fullname, extension)
    filename = "%s_%s_%s.%s" % (filename, final_width, final_height,
                             extension)

    cache_dir_name = getattr('settings', 'RESPONSIVE_IMAGES_CACHE_DIR',
                             'responsive_images_cache')
    cache_path = os.path.join(settings.MEDIA_ROOT, cache_dir_name)
    if not finders.find(cache_dir_name):
        os.chdir(settings.MEDIA_ROOT)
        call(['mkdir', cache_dir_name])
    os.chdir(cache_path)

    if not finders.find(cache_dir_name + "/" + filename):
        size = (final_width, final_height)
        resized_image = i.resize(size, Image.ANTIALIAS)
        resized_image.save(filename, extension,
            quality=getattr('settings', cache_dir_name, 75)) 

    # Return resized image
    return get_file(filename, extension)

