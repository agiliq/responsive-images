from django.conf import settings

from responsive_images.utils import (
    get_final_resolution, get_file, get_resized_image
)


def adapt_image(request):
    final_resolution = get_final_resolution(request)

    filename = request.META['QUERY_STRING'].replace(settings.IMAGE_ENDS_WITH, "")

    if filename.find(settings.STATIC_URL) == 0:
        filename = filename[len(settings.STATIC_URL):]
    elif filename.find(settings.MEDIA_URL) == 0:
        filename = filename[len(settings.MEDIA_URL):]
    else:
        return None

    resized_filename, extension = get_resized_image(filename, final_resolution)

    # Return resized image
    return get_file(resized_filename, extension)
