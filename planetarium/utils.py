import os
import uuid

from django.utils.text import slugify


def astronomy_show_image_file_path(instance, filename):
    """A function to generate the image file path for the astronomy show."""

    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/", filename)
