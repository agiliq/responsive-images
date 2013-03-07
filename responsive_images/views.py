# Create your views here.
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.conf import settings

from responsive_images.utils  import get_final_resolution

from PIL import Image

import os
from subprocess import call


def adapt_image(request):
    resolutions = [1382, 992, 768, 480]
    final_resolution = resolutions[0]
    try:
        resolutions = settings.RESPONSIVE_IMAGE_RESOLUTIONS
    except AttributeError:
        pass
    try:
        resolution = int(request.COOKIES['resolution'])
        final_resolution = get_final_resolution(resolution, resolutions)
    except KeyError:
        final_resolution = 100



    filename = request.META['QUERY_STRING']

    fullname = settings.PROJECT_PATH + filename
    filename = filename.split("/").pop()
    filename, extension = filename.split(".")
    filename = "%s_%s_%s.%s" % (filename, final_resolution, final_resolution,
                             extension)

    if not os.path.exists(settings.PROJECT_PATH+'/static/responsive_images_cache'):
        os.chdir(settings.PROJECT_PATH+'/static')
        call(['mkdir', 'responsive_images_cache'])
    os.chdir(settings.PROJECT_PATH+'/static/responsive_images_cache')

    image = Image.open(fullname)
    if not os.path.exists(filename):
        resized_image = image.resize((final_resolution, final_resolution), Image.ANTIALIAS)
        resized_image.save(filename, extension, quality=75)


    try:
        f = file(filename, "rb")
    except Exception, e:
        return HttpResponse(str(e))

    #Return resized image
    wrapper = FileWrapper(f)
    response = HttpResponse(wrapper, mimetype="image/jpeg")
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

