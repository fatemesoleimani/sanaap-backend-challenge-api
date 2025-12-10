from PIL import Image
from rest_framework import serializers


def validate_image_file(file):
    if not file.content_type.startswith("image/"):
        raise serializers.ValidationError("Only image files are allowed.")
    try:
        img = Image.open(file)
        img.verify()
    except Exception:
        raise serializers.ValidationError("Invalid or corrupted image file.")
    valid_extensions = ["jpg", "jpeg", "png", "gif", "webp"]
    ext = file.name.split(".")[-1].lower()
    if ext not in valid_extensions:
        raise serializers.ValidationError("Unsupported image format.")
    return file
