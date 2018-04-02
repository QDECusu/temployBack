from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import json

def is_json(value):
    """
    Validate json array
    """
    print(value)
    try:
        parsed_json = json.loads(value)
        if type(parsed_json) is list:
            return
        else:
            raise Exception("It's a dictionary, not a list")
        # If we're here it didn't throw any error
        return
    except Exception as e:
        raise ValidationError("The input is not valid JSON, please input a valid json array", status='invalid' )
