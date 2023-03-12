from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from six import string_types
from stdnum import isbn


# Thanks secnot: https://github.com/secnot/django-isbn-field/blob/master/isbn_field/validators.py
def isbn_validator(raw_isbn):
    """ Check string is a valid ISBN number"""
    isbn_to_check = raw_isbn.replace('-', '').replace(' ', '')

    if not isinstance(isbn_to_check, string_types):
        raise ValidationError("Invalid ISBN: Not a string")

    if len(isbn_to_check) != 10 and len(isbn_to_check) != 13:
        raise ValidationError("Invalid ISBN: Wrong length")

    if not isbn.is_valid(isbn_to_check):
        raise ValidationError("Invalid ISBN: Failed checksum")

    if isbn_to_check != isbn_to_check.upper():
        raise ValidationError("Invalid ISBN: Only upper case allowed")

    return True

ALLOWED_DOMAINS_PATTERN = r"(s4\.anilist\.co|images-na\.ssl-images-amazon\.com|static\.wikia\.nocookie\.net\/.*\/images|m\.media-amazon\.com\/images|cdn\.myanimelist\.net\/images|uploads\.mangadex\.org\/covers|i\.gr-assets\.com\/images|comicvine\.gamespot\.com\/a\/uploads|dw9to29mmj727\.cloudfront\.net)"

image_url_validator = RegexValidator(
    regex=fr"^https?:\/\/{ALLOWED_DOMAINS_PATTERN}\/",
    message="The image must be from one of the trusted sites. Learn more about this on the contribution guidelines."
)
