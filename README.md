What is this
--------------

Responsive design requires *responsive images*. Images which adapt their size depending upon what device you are using.
This app provides this.

Usage
-----------

Add RESPONSIVE_IMAGE_RESOLUTIONS to settings with an array of image sizes required as per resolution.  

Example:

    RESPONSIVE_IMAGE_RESOLUTIONS = [1300, 1200, 1100, 800, 500]

From above values, if the resolution lies between 1300 and 1200, then the image of width 1200 will be shown.

Add this to the head section of your template.

     <script>document.cookie='resolution='+Math.max(window.outerWidth, 0)+'; path=/';</script>


Add this to the start of your template.

    {% load responsive_images_tags %}


If you are using a static file.

    <img src="{% static_responsive 'img/logo.png' %}" />


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
