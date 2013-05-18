from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse

import os


def get_final_resolution(resolution):
    resolution = int(resolution)
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
    if resolution < resolutions[-1]:
        final_resolution = resolutions[-1]
        #final_resolution = resolution
    final_resolution = final_resolution - 50
    return final_resolution


def get_file(filename, extension):
    f = file(filename, "rb")
    wrapper = FileWrapper(f)
    if extension not in ['png', 'jpg', 'jpeg', 'gif']:
        mimetype = 'image/jpeg'
    else:
        mimetype = 'image/%s' % extension
    response = HttpResponse(wrapper, mimetype=mimetype)
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response
