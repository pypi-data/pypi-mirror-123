import os
import json

from alfa_sdk.common.stores import ConfigStore
from alfa_sdk.common.helpers import AlfaConfigHelper
from alfa_sdk.common.exceptions import AlfaConfigError
from alfa_cli.common.exceptions import RuntimeError
from alfa_cli.lib.runner.node import NodeRunner
from alfa_cli.lib.runner.python import PythonRunner
from alfa_cli.lib.runner.utils import evaluate_reference


class LocalRunner:
    def __init__(
        self,
        obj,
        spec_path,
        function_id,
        environment_name,
        function_name="invoke",
        function_type="algorithm",
    ):
        self.function_type = function_type
        self.function_name = function_name

        self.set_auth(obj)
        self.config = AlfaConfigHelper.load(os.path.join(".", spec_path), is_package=False)
        self.function_config = self.get_function_config()
        self.runner = self.create_runner()

        self.function_id = self.parse_function_id(function_id)
        self.environment_name = self.parse_environment_name(environment_name)
        self.environment_id = f"{self.user['teamId']}:{self.function_id}:{self.environment_name}"
        self.context = self.get_context()

    #

    def set_auth(self, obj):
        try:
            client = obj["client"]()
            self.user = client.user
            self.token = client.session.auth.token
        except:
            self.user = {"userId": "test_user_id", "teamId": "test_team_id"}
            self.token = "test_token"

    def get_context(self):
        alfa_environment = ConfigStore.get_value("alfa_env", group="alfa", default="prod")
        alfa_id = ConfigStore.get_value("alfa_id", group="alfa", default="public")
        platform_region = ConfigStore.get_value("platform_region", group="alfa", default="eu-central-1")

        context = {
            "userId": self.user["userId"],
            "teamId": self.user["teamId"],
            "alfaEnvironment": alfa_environment,
            "alfaID": alfa_id,
            "platformRegion": platform_region,
            "algorithmRunId": -1,
            "token": self.token,
            "accessToken": self.token,
            "auth0Token": self.token,
            "__RUN_LOCAL__": True,
        }

        if self.function_type == "algorithm":
            context["algorithmEnvironmentId"] = self.environment_id

        if self.function_type == "integration":
            context["integrationId"] = self.function_id
            context["environmentName"] = self.environment_name
            context["functionName"] = self.function_name

        os.environ["ALFA_CONTEXT"] = json.dumps(context)
        return context

    #

    def parse_function_id(self, function_id=None):
        if not function_id:
            function_id = self.config.get("id", os.path.dirname(os.getcwd()))
        return function_id

    def parse_environment_name(self, environment_name=None):
        if not environment_name:
            environment_name = self.config.get("environment", "development")
        return environment_name

    def get_function_config(self):
        ERROR_MESSAGE = f"{self.function_name} function not defined"

        functions = self.config.get("functions")
        if not functions:
            raise AlfaConfigError(message="Invalid configuration", error=ERROR_MESSAGE)

        invoke_functions = [func for func in functions if self.function_name in func.keys()]
        if len(invoke_functions) == 0:
            raise AlfaConfigError(message="Invalid configuration", error=ERROR_MESSAGE)

        invoke_function = invoke_functions[0]
        return invoke_function[self.function_name]

    def get_runtime(self):
        ERROR_MESSAGE = "runtime not defined"

        provider = self.function_config.get("provider")
        if not provider:
            raise AlfaConfigError(message="Invalid configuration", error=ERROR_MESSAGE)

        runtime = provider.get("runtime")
        if not runtime:
            raise AlfaConfigError(message="Invalid configuration", error=ERROR_MESSAGE)

        return runtime

    #

    def create_runner(self):
        runtime = self.get_runtime()

        if "python" in runtime:
            return PythonRunner(self.function_config, self.function_name, self.function_type)

        if "node" in runtime:
            return NodeRunner(self.function_config, self.function_name, self.function_type)

        raise RuntimeError(message=f"Runtime '{runtime}' not supported")

    def run(self, problem, to_profile=False, profile_sort=None):
        if self.function_name in ["build", "score"]:
            problem = evaluate_reference(problem)

        problem["context"] = {**self.context, **problem.get("context", {})}
        res = self.runner.run(problem, to_profile, profile_sort)

        try:
            res = json.loads(res)
        except:
            pass

        return res
