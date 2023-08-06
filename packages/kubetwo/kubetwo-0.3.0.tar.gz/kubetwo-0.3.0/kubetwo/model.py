import json
import os
from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, conint, constr, root_validator, validator

from kubetwo.config import ArtifactSettings, Settings
from kubetwo.validator import Validator


class CLICreateInput(BaseModel):

    cluster_name: constr(min_length=1, max_length=64)
    ami: str = Settings.DEFAULT_AMI
    instance_type: str = Settings.DEFAULT_INSTANCE_TYPE
    availability_zone: str = None
    control_plane: conint(ge=1) = Settings.DEFAULT_CONTROL_PLANE_NUM
    worker_node: conint(ge=1) = Settings.DEFAULT_WORKER_NODE_NUM
    open_ports: List[conint(ge=-1, le=65535)] = Settings.DEFAULT_OPEN_PORTS
    approve: bool = False

    _is_credentials_registered = root_validator(pre=True, allow_reuse=True)(Validator.is_credentials_registered)

    _is_ssh_keys_registered = root_validator(pre=True, allow_reuse=True)(Validator.is_ssh_keys_registered)

    _is_ssh_keys_exist = root_validator(pre=True, allow_reuse=True)(Validator.is_ssh_keys_exist)

    @validator("availability_zone")
    def set_default_availability_zone(cls, v):
        aws_default_region = os.environ.get("AWS_DEFAULT_REGION")
        if aws_default_region and not v:
            v = aws_default_region + "a"
        return v

    @validator("open_ports")
    def prohibit_port_0(cls, v):
        if 0 in v:
            raise ValueError("Port 0 is not allowed")
        return v


class CLIScaleInput(BaseModel):
    
    cluster_name: constr(min_length=1, max_length=64)
    worker_node: conint(ge=1)
    approve: bool = False

    _is_credentials_registered = root_validator(pre=True, allow_reuse=True)(Validator.is_credentials_registered)

    _is_ssh_keys_registered = root_validator(pre=True, allow_reuse=True)(Validator.is_ssh_keys_registered)

    _is_ssh_keys_exist = root_validator(pre=True, allow_reuse=True)(Validator.is_ssh_keys_exist)

    _artifact_dir_exists = root_validator(pre=True, allow_reuse=True)(Validator.artifact_dir_exists)

    _tfstate_exists = root_validator(pre=True, allow_reuse=True)(Validator.tfstate_exists)

    _input_json_exists = root_validator(pre=True, allow_reuse=True)(Validator.input_json_exists)

    _is_input_json_valid = root_validator(allow_reuse=True)(Validator.is_input_json_valid)

    @validator("worker_node")
    def is_worker_node_changed(cls, v, values):
        with open(ArtifactSettings(values["cluster_name"]).INPUT_JSON_FILE_PATH, "r") as f:
            current_worker_node = json.load(f).get("worker_node")
        if v == current_worker_node:
            raise ValueError(f"Number of worker node should be changed (current value is {v}).")
        return v

    def scale_type(self) -> str:
        with open(ArtifactSettings(self.cluster_name).INPUT_JSON_FILE_PATH, "r") as f:
            input_json = json.load(f)
        return "out" if self.worker_node > input_json["worker_node"] else "in"

    def dict_all(self) -> Dict:
        with open(ArtifactSettings(self.cluster_name).INPUT_JSON_FILE_PATH, "r") as f:
            input_json = json.load(f)
        input_json.update(self.dict())
        input_json["scale_type"] = self.scale_type()
        return input_json


class CLIDeleteInput(BaseModel):

    cluster_name: constr(min_length=1, max_length=64)
    approve: bool = False

    _is_credentials_registered = root_validator(pre=True, allow_reuse=True)(Validator.is_credentials_registered)

    _is_ssh_keys_registered = root_validator(pre=True, allow_reuse=True)(Validator.is_ssh_keys_registered)

    _is_ssh_keys_exist = root_validator(pre=True, allow_reuse=True)(Validator.is_ssh_keys_exist)

    _artifact_dir_exists = root_validator(pre=True, allow_reuse=True)(Validator.artifact_dir_exists)

    _tfstate_exists = root_validator(pre=True, allow_reuse=True)(Validator.tfstate_exists)


class CreateInput(BaseModel):

    cluster_name: str
    ami: str
    instance_type: str
    availability_zone: str
    control_plane: int
    worker_node: int
    open_ports: List[int]
    approve: bool


class ScaleInput(BaseModel):
    
    cluster_name: str
    ami: str
    instance_type: str
    availability_zone: str
    control_plane: int
    worker_node: int
    open_ports: List[int]
    approve: bool


class DeleteInput(BaseModel):

    cluster_name: str
    approve: bool
