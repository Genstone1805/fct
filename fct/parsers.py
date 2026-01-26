"""
Custom parsers that ensure recursive camelCase to snake_case conversion
for nested form data and JSON data.
"""
from djangorestframework_camel_case.parser import (
    CamelCaseFormParser,
    CamelCaseMultiPartParser,
    CamelCaseJSONParser,
)
from djangorestframework_camel_case.util import underscoreize


def recursive_underscoreize(data):
    """
    Recursively convert all keys in nested data structures from camelCase to snake_case.
    Handles dicts, lists, and nested combinations.
    """
    if isinstance(data, dict):
        # First underscoreize the top-level keys, then recursively process values
        underscored = underscoreize(data)
        return {key: recursive_underscoreize(value) for key, value in underscored.items()}
    elif isinstance(data, list):
        return [recursive_underscoreize(item) for item in data]
    else:
        return data


class RecursiveCamelCaseFormParser(CamelCaseFormParser):
    """
    Form parser that recursively converts all nested camelCase keys to snake_case.
    """
    def parse(self, stream, media_type=None, parser_context=None):
        data = super().parse(stream, media_type, parser_context)
        # Ensure nested data is also converted
        # Use .dict() for QueryDict to get single values instead of lists
        if hasattr(data, 'data'):
            if hasattr(data.data, 'dict'):
                data.data = recursive_underscoreize(data.data.dict())
            else:
                data.data = recursive_underscoreize(data.data)
        return data


class RecursiveCamelCaseMultiPartParser(CamelCaseMultiPartParser):
    """
    MultiPart parser that recursively converts all nested camelCase keys to snake_case.
    """
    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(stream, media_type, parser_context)
        # Ensure nested data is also converted
        # Use .dict() for QueryDict to get single values instead of lists
        if hasattr(result, 'data'):
            if hasattr(result.data, 'dict'):
                result.data = recursive_underscoreize(result.data.dict())
            else:
                result.data = recursive_underscoreize(result.data)
        return result


class RecursiveCamelCaseJSONParser(CamelCaseJSONParser):
    """
    JSON parser that recursively converts all nested camelCase keys to snake_case.
    """
    def parse(self, stream, media_type=None, parser_context=None):
        data = super().parse(stream, media_type, parser_context)
        # Ensure nested data is also converted
        return recursive_underscoreize(data)
