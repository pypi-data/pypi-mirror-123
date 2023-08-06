import os
from .utils.misc import singleton
from .controller import HyperControlClient
from subprocess import Popen, PIPE
from .utils.log import logger


@singleton
class Hyper(object):
    def __init__(self, local: bool = True, git: str = None, user_id: str = "admin"):
        self.local = local
        self.git = git
        self.user_id = user_id

    def _hardware(self, pu: str, pu_count: int, spot: bool, local: bool):
        """
        Construct hardware choice
        #TODO Change to aws machine types
        """
        hardware = {}
        assert pu in ["cpu", "v100", "k80"]

        if pu == "cpu":
            assert pu_count in [2, 4, 8, 16, 48, 96]
            hardware[pu] = pu_count

        if pu == "k80":
            assert pu_count in [1, 8, 16]
            hardware["gpu"] = pu
            hardware["gpu_count"] = pu_count

        if pu == "v100":
            assert pu_count in [1, 4, 8]
            hardware["gpu"] = pu
            hardware["gpu_count"] = pu_count

        if spot:
            hardware["spot"] = spot

        if local:
            hardware["local"] = local

        return hardware

    def down(self, experiment_id: str) -> dict:
        # TODO writer parser
        if self.local:
            # TODO kill the local process
            return {"resp": "running local"}

        resp = HyperControlClient(username=self.user_id).down(experiment_id)
        return resp

    def get_experiment(self, experiment_id: str) -> dict:
        # TODO writer parser
        if self.local:
            # TODO mimic running experiment and get logs
            return {}
        exp = HyperControlClient(username=self.user_id).list_experiment(experiment_id)
        return exp

    def get_task(self, task_id: str) -> dict:
        # TODO writer parser
        task = HyperControlClient(username=self.user_id).list_task(task_id)
        return task

    def up(
        self,
        command: list,
        pu: str,  # cpu, v100, k80
        parameters: dict = {},
        pu_count: int = 1,
        workers: int = 1,
        samples: int = 1,
        spot: bool = False,
        local: bool = False,
        recovery: bool = False,
        docker: str = "tensorflow/tensorflow:latest",
        private_docker: bool = False,
        name: str = "experiment_tag",
    ) -> str:
        """
        Can start multiple instances on aws and execute specific code inside docker

        INPUTS:
            command - contains list of bash commands e.g. [ "sleep 10", "echo {{batch_size}}"]
            parameters - contains dictionary of parameters (both static and dynamic) examples here.
                        parameters get replaced inside command for each task
                        {
                            'batch_size': {'range': 0-4, 'sampling': 'discrete'},
                            'lr': {'range': 0.1-0.3, 'sampling': 'uniform'},
                            'networks': ['cnn', 'rnn', 'kebonn']
                        }
            pu and pu_count - provide hardware specifications. Here are possible combinations
                    ('cpu', 2): 'm5.large',
                    ('cpu', 4): 'm5.xlarge',
                    ('cpu', 8): 'm5.2xlarge',
                    ('cpu', 16):'m5.4xlarge',
                    ('cpu', 48):'m5.12xlarge',
                    ('cpu', 96):'m5.24xlarge',
                    ('k80', 1): 'p2.xlarge',
                    ('k80', 8): 'p2.8xlarge',
                    ('k80', 16): 'p2.16xlarge',
                    ('v100', 1): 'p3.2xlarge',
                    ('v100', 4): 'p3.8xlarge',
                    ('v100', 8): 'p3.16xlarge'
            workers - number of workers
            samples - number of samples
            spot - to use spot instances
            local - to ask the server to run a local service
            recovery - recover a task in case of failure
            docker - the image to run
        """
        if self.git is not None:
            gitcommand = [
                "git pull --recurse-submodules",
                "git reset --hard {}".format(self.git),
            ]
            command = gitcommand + command

        experiment = {
            "image": docker,
            "parameters": parameters,
            "hardware": self._hardware(pu, pu_count, spot, local),
            "command": command,
            "workers": workers,
            "samples": samples,
            "recovery": recovery,
            "image_access": "private" if private_docker else "public",
        }

        recipe = {"experiments": {name: experiment}}
        logger.info(recipe)
        if self.local:
            # os.system(" & ".join(command))
            p = Popen(command, shell=True)
            # res = p.stdout.read()
            # logger.info(res)
        else:
            resp = HyperControlClient(username=self.user_id).upload(recipe)
            return resp[0]
        return {"ID": ""}


if __name__ == "__main__":

    hashcode = "somehash"
    args = ""
    command = [
        "git pull --recurse-submodules",
        "git reset --hard {}".format(hashcode),
        "python3 train/train.py {}".format(args),
    ]

    # Start a k80 instance and train
    resp = Hyper().up(
        name="mnist",
        docker="pytorch/pytorch:latest",
        pu="k80",
        command=["python examples/mnist/main.py"],
    )
    print(resp)
