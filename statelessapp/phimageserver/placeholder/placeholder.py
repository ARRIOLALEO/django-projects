import os
import sys
from django.conf import settings
from django.urls.resolvers import URLPattern

DEBUG = os.environ.get("DEBUG", "on") == "on"

SECRET_KEY = os.environ.get("SECRET_KEY", "kjhsdkfkjabdf4564#$%@#$")

ALLOWED_HOST = os.environ.get("ALLOWED_HOST", "localhost").split(",")


settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOST=ALLOWED_HOST,
    ROOT_URLCONF=__name__,
    MIDLEWARE_CLASSES=(
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ),
)

import hashlib
from django import forms
from io import BytesIO
from PIL import Image, ImageDraw
from django.conf.urls import url
from django.core.cache import cache
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import etag


def index():
    return HttpResponse("this is the main page of our aplication")


class ImageForm(forms.Form):
    """thi for it is for validate the request placeholder image"""

    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)

    def generate(self, image_format="PNG"):
        """generate an image of the giving type and returns as raw bytes."""
        height = self.cleaned_data["height"]
        width = self.cleaned_data["width"]
        key = "{}.{}.{}".format(width.height, image_format)
        content = cache.get(key)
        if content is None:
            image = Image.new("RGB", (width, height))
            draw = ImageDraw.Draw(image)
            text = "{} x {}".format(width, height)
            textwidth, textheight = draw.textsize(text)
        if textwidth < width and textheight < height:
            texttop = (height - textheight) // 2
            textleft = (width - textwidth) // 2
            draw.text((textleft, texttop), text, fill=(255, 255, 255))
        content = BytesIO()
        image.save(content, image_format)
        content.seek(0)
        return content

def generate_etag(request, width, height):
    content = 'Placeholder:{0} x {1}'.format(width,height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()

@etag(generate_etag)
def placeholder(request, width, height):
    form = ImageForm({"height": height, "width": width})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type="image/png")
    else:
        return HttpResponse("the image is not the right size")


application = get_wsgi_application()

urlpatterns = (
    url(
        r"^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$",
        placeholder,
        name="placeholder",
    ),
    url(r"^$", index, name="homepage"),
)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
