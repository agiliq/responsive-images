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

    if max(i.size[0], i.size[1]) < final_resolution:
        return get_file(fullname, extension)
    filename = "%s_%s_%s.%s" % (filename, final_resolution, final_resolution,
                             extension)

    cache_path = os.path.join(settings.MEDIA_ROOT, settings.RESPONSIVE_IMAGES_CACHE_DIR)
    if not finders.find(settings.RESPONSIVE_IMAGES_CACHE_DIR):
        os.chdir(settings.MEDIA_ROOT)
        call(['mkdir', settings.RESPONSIVE_IMAGES_CACHE_DIR])
    os.chdir(cache_path)

    image = Image.open(fullname)
    if not finders.find(settings.RESPONSIVE_IMAGES_CACHE_DIR+"/"+filename):
        resized_image = image.resize((final_resolution, final_resolution), Image.ANTIALIAS)
        resized_image.save(filename, extension, quality=75)

    # Return resized image
    return get_file(filename, extension)

