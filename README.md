What is this
--------------

Responsive design requires *response images*. Images which adapt their size depending upon what device you are using.
This app provides this.

Usage
-----------

Add this to the start of your template.

    {% load responsive_images_tags %}

If you are using a media file:

    {% responsive item.image as im %}
        <img src="{{ im.url }}" width="{{ im.width }}" height="{{ im.height }}" />
    {% endresponsive %}


If you are using a static file.

    <img src="{% sttaic_responsive 'img/logo.png' %}" />



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
