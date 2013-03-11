from django.conf import settings


def get_final_resolution(resolution):
    resolution = int(resolution)
    try:
        resolutions = settings.RESPONSIVE_IMAGE_RESOLUTIONS
    except AttributeError:
        resolutions = [1382, 992, 768, 480]
    final_resolution = resolutions[0]
    if resolution < resolutions[0]:
        for r in resolutions:
            if resolution > r:
                final_resolution = r
                break
    if resolution < resolutions[-1]:
        final_resolution = resolutions[-1]
        #final_resolution = resolution
    final_resolution = final_resolution-50
    return final_resolution
