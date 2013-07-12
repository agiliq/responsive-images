[![Build Status](https://travis-ci.org/agiliq/responsive-images.png?branch=master)](https://travis-ci.org/agiliq/responsive-images)

What is this
--------------

Responsive design requires *responsive images*. Images which adapt their size depending upon what device you are using.
This app provides this.

Usage
-----------

Settings: 
* RESPONSIVE_IMAGE_RESOLUTIONS to settings with an array of image sizes required as per resolution.  
* IMAGE_ENDS_WITH (A string): Image urls ending with this string will be made responsive.

Optional Settings:
* RESPONSIVE_IMAGES_CACHE_DIR = Defaults to 'responsive_images_cache'.
 Resized images will be placed in this directory.
* RESPONSIVE_IMAGE_QUALITY: Defaults to 75. This is used while resizing the original image.
* RESPONSIVE_IMAGE__FOR_TEST: This is required when testing. 

Example:

    RESPONSIVE_IMAGE_RESOLUTIONS = [1300, 1200, 1100, 800, 500]

From above values, if the resolution lies between 1300 and 1200, then the image of width 1200 will be shown.

Add this to the head section of your template.

     <script>document.cookie='resolution='+Math.max(window.outerWidth, 0)+'; path=/';</script>


Add this to the start of your template.

    {% load responsive_images_tags %}


If you are using a static file.

    <img src="{% static_responsive 'img/logo.png' %}" />

If you are using a media file.

    <img src="{% static_responsive instance.fieldname %}" />


Modify your nginx configuration(or related) as below:

    Please do a permanent redirect to all the files ending with "___asnf874wthwengsfduy".

This can be done via nginx as follows:

    rewrite (___asnf874wthwengsfduy)$ /adapt-image?$request_uri? permanent;



Installations
-------------------
* pip install -r requirements.txt
* add `responsive_images` to installed apps.

Todo
------
* Add Test
* Add travis build metadata

License
---------
3 clause BSD
