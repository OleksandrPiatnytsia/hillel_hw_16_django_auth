import logging


class HideClientErrorTraceback(logging.Filter):
    """Drops the traceback from django.request records about 4xx responses.

    Django logs a 403 (PermissionDenied) with the full exception traceback,
    although it's a normal "access denied", not a bug in our code. The
    one-line message ("Forbidden (Permission denied): /create/") is enough.
    5xx records (real errors) keep their traceback.
    """

    def filter(self, record):
        # django.request puts the response status into record.status_code
        status_code = getattr(record, "status_code", None)
        if status_code is not None and status_code < 500:
            record.exc_info = None
            record.exc_text = None  # cached formatted traceback, if any
        return True  # never drop the record itself, only shorten it
