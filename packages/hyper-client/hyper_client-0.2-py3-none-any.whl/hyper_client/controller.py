import json
import os
from . import config
from .utils.log import logger
from .base import SnarkHttpClient
from .utils.exceptions import SnarkException
import pprint


class HyperControlClient(SnarkHttpClient):
    """
    Controlling Snark Pods through rest api
    """

    def __init__(self, username):
        super(HyperControlClient, self).__init__()
        self.auth = (username, "")

    def upload(self, descriptor):
        desc = {"descriptor": json.dumps(descriptor)}
        response = self.request(
            "POST",
            config.UP_DESCRIPTOR_SUFFIX,
            auth=self.auth,
            endpoint=config.HYPER_ENDPOINT,
            json=desc,
        )
        return response.json()

    def down(self, name_id):
        response = self.request(
            "POST",
            config.DOWN_DESCRIPTOR_SUFFIX,
            auth=self.auth,
            endpoint=config.HYPER_ENDPOINT,
            json=[name_id],
        )
        return response.json()

    def list(self, all):
        suffix = (
            config.LIST_EXPERIMENTS_SUFFIX
            if all
            else config.LIST_EXPERIMENTS_RUNNING_SUFFIX
        )
        response = self.request(
            "GET", suffix, auth=self.auth, endpoint=config.HYPER_ENDPOINT
        )
        return response.json()

    def list_experiment(self, experiment_id):
        data = {"experiment_id": experiment_id}
        response = self.request(
            "GET",
            config.LIST_EXPERIMENT_SUFFIX,
            auth=self.auth,
            endpoint=config.HYPER_ENDPOINT,
            json=data,
        )
        return response.json()

    def list_task(self, task_id):
        data = {"task_id": task_id}
        response = self.request(
            "GET",
            config.LIST_EXPERIMENT_BY_TASK_SUFFIX,
            auth=self.auth,
            endpoint=config.HYPER_ENDPOINT,
            json=data,
        )
        return response.json()
