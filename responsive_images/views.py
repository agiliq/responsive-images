from django.conf import settings

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

    filename = request.META['QUERY_STRING'].replace("___asnf874wthwengsfduy", "")

    fullname = settings.STATIC_ROOT + filename[len(settings.STATIC_URL)-1:]
    filename = filename.split("/").pop()
    filename, extension = filename.split(".")
    i = Image.open(fullname)

    if max(i.size[0], i.size[1]) < final_resolution:
        return get_file(fullname, extension)
    filename = "%s_%s_%s.%s" % (filename, final_resolution, final_resolution,
                             extension)

    if not os.path.exists(settings.STATIC_ROOT+'/responsive_images_cache'):
        os.chdir(settings.STATIC_ROOT)
        call(['mkdir', 'responsive_images_cache'])
    os.chdir(settings.STATIC_ROOT+'/responsive_images_cache')

    image = Image.open(fullname)
    if not os.path.exists(filename):
        resized_image = image.resize((final_resolution, final_resolution), Image.ANTIALIAS)
        resized_image.save(filename, extension, quality=75)

    # Return resized image
    return get_file(filename, extension)

