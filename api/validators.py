from django.core.exceptions import ValidationError
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
