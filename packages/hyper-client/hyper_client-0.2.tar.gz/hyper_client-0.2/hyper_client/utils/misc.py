from flask import Response
import json as old_json
import ujson as json
import decimal
import time
import string
import random
import uuid
import os


class _SingletonWrapper:
    """
    A singleton wrapper class. Its instances would be created
    for each decorated class.
    """

    def __init__(self, cls):
        self.__wrapped__ = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        """Returns a single instance of decorated class"""
        if self._instance is None:
            self._instance = self.__wrapped__(*args, **kwargs)
        return self._instance


def display_progress(current, max):
    progress = 100 * float(current) / float(max)
    progress = int(abs(progress))
    progress = progress if progress < 100 else 100
    print("~~~ progress={} ~~~".format(progress))


def singleton(cls):
    """
    A singleton decorator. Returns a wrapper objects. A call on that object
    returns a single instance object of decorated class. Use the __wrapped__
    attribute to access decorated class directly in unit tests
    """
    return _SingletonWrapper(cls)


def responsify(data={}, status=200, err=""):
    if not err == "" or status == 400:
        data = {"status": "failed", "description": "illegal payload format."}
        status = 400
        if not err == "":
            data["description"] = str(err)

    return Response(
        response=json.dumps(data),  # , cls=DecimalEncoder),
        status=status,
        mimetype="application/json",
    )


class DecimalEncoder(old_json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def get_timestamp():
    return str(time.time())


def id_generator(size=6, chars=string.ascii_lowercase):
    return "".join(random.choice(chars) for _ in range(size)) + "-" + str(uuid.uuid4())
