import json
import os
from pathlib import Path
import subprocess
from typing import Dict, List, Tuple

from jinja2 import Template
from pydantic import BaseModel
from termcolor import cprint

from kubetwo.config import Settings
from kubetwo.exception import *


class Common:

    @classmethod
    def run_command(cls, command: str, cwd: str=None, stdout: bool=True):
        stdout = None if stdout else subprocess.DEVNULL
        try:
            process = subprocess.run(
                command, 
                shell=True, 
                stdout=stdout, 
                stderr=subprocess.PIPE,
                cwd=cwd
            )
            process.check_returncode()
        except subprocess.CalledProcessError:
            raise ProcessException(process.stderr.decode("utf8"))
        
    @classmethod
    def get_node_info(cls, rendered_tfstate_path: Path) -> Tuple[List[Dict], List[Dict]]:
        """Load node information on AWS from terraform.tfstate.
           Each item format is {"name": str, "private_ip": str, "public_ip": str}."""
        if not os.path.exists(str(rendered_tfstate_path)):
            raise TerraformStateNotFound(f"""
                [ERROR] terraform.tfstate doesn't exist at {str(rendered_tfstate_path)}
                It's necessary to execute kubetwo init command first""")

        with open(rendered_tfstate_path, "r") as file:
            tfstate_data = json.load(file)

        control_plane_private_ip_list = tfstate_data["outputs"]["control_plane_private_ip"]["value"]
        control_plane_public_ip_list = tfstate_data["outputs"]["control_plane_public_ip"]["value"]
        worker_node_private_ip_list = tfstate_data["outputs"]["worker_node_private_ip"]["value"]
        worker_node_public_ip_list = tfstate_data["outputs"]["worker_node_public_ip"]["value"]

        control_plane_list = []
        for i, (private_ip, public_ip) in enumerate(zip(control_plane_private_ip_list, control_plane_public_ip_list)):
            name = f"control-plane{i}"
            control_plane_list.append({"name": name, "private_ip": private_ip, "public_ip": public_ip})

        worker_node_list = []
        for i, (private_ip, public_ip) in enumerate(zip(worker_node_private_ip_list, worker_node_public_ip_list)):
            name = f"worker-node{i}"
            worker_node_list.append({"name": name, "private_ip": private_ip, "public_ip": public_ip})

        return control_plane_list, worker_node_list
    
    @classmethod
    def get_default_user_name(cls, rendered_tfstate_path: Path) -> str:
        with open(rendered_tfstate_path, "r") as f:
            tfstate_data = json.load(f)

        ami_name = tfstate_data["outputs"]["ami_name"]["value"]
        ami_description = tfstate_data["outputs"]["ami_description"]["value"]
        ami_location = tfstate_data["outputs"]["ami_location"]["value"]

        with open(Settings.DISTRO_INFO_FILE_PATH, "r") as file:
            distro_list = json.load(file)

        default_user_name = "ec2-user"
        for distro in distro_list:
            if  (
                distro["ami_name_keyword"] in ami_name or
                distro["ami_description_keyword"] in ami_description or
                distro["ami_location_keyword"] in ami_location
                ):
                distro_name = distro["distro_name"]
                cprint(f"{distro_name} is detected.")
                default_user_name = distro["user_name"]
                break
                
        cprint(f"User \"{default_user_name}\" will be used for EC2 default user.\n")
        return default_user_name

    @classmethod
    def create_node_info(cls, 
        rendered_tfstate_path: Path,
        rendered_node_info_path: Path
    ):
        control_plane_list, worker_node_list = cls.get_node_info(rendered_tfstate_path)
        user_name = cls.get_default_user_name(rendered_tfstate_path)
        params = {
            "control_plane_list": control_plane_list,
            "worker_node_list": worker_node_list,
            "user_name": user_name,
            "ssh_private_key": str(Common.get_ssh_private_key_path())
        }
        with open(Settings.NODE_INFO_FILE_PATH, "r") as file:
            template = Template(file.read())

        node_info = template.render(params)

        with open(rendered_node_info_path, "w") as file:
            file.write(node_info)

        cprint(node_info, "cyan")

    @classmethod
    def save_input_info(cls, input_json_path: Path, *inputs: BaseModel):
        merged_dict = {}
        for input in inputs:
            input_dict = json.loads(input.json())
            merged_dict = {**merged_dict, **input_dict}

        with open(input_json_path, "w") as f:
            json.dump(merged_dict, f, indent=4)

    @classmethod
    def get_ssh_public_key_path(cls):
        return Path(os.environ.get("SSH_PUBLIC_KEY_PATH")).expanduser()

    @classmethod
    def get_ssh_private_key_path(cls):
        return Path(os.environ.get("SSH_PRIVATE_KEY_PATH")).expanduser()
