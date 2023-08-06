import json
import sys
from typing import List

import fire
from pydantic import ValidationError
from termcolor import cprint

from kubetwo.create import Create
from kubetwo.scale import ScaleIn, ScaleOut
from kubetwo.delete import Delete
from kubetwo.model import *
from kubetwo.config import Settings
from kubetwo.exception import *
from kubetwo.validator import ValidationFormatter


def main():
    fire.Fire(CLI)


class CLI:

    @classmethod
    def create(
        cls,
        cluster_name: str,
        ami: str=Settings.DEFAULT_AMI,
        instance_type: str=Settings.DEFAULT_INSTANCE_TYPE,
        availability_zone: str=None,
        control_plane: int=Settings.DEFAULT_CONTROL_PLANE_NUM,
        worker_node: int=Settings.DEFAULT_WORKER_NODE_NUM,
        open_ports: List[int] = Settings.DEFAULT_OPEN_PORTS,
        approve: bool = False,
    ):
        try:
            cli_create_input = CLICreateInput(
                cluster_name = cluster_name,
                ami = ami,
                instance_type = instance_type,
                availability_zone = availability_zone,
                control_plane = control_plane,
                worker_node = worker_node,
                open_ports = open_ports,
                approve = approve
            )
            create_input = CreateInput(**cli_create_input.dict())
            Create(create_input).run()

        except ValidationError as e:
            cprint("[ERROR] Input value is not correct.", "red")
            validation_result = json.loads(e.json())
            cprint(ValidationFormatter.format(validation_result), "red")
            sys.exit(1)
        except (CheckDeniedException, TerraformStateNotFound) as e:
            cprint(e, "red")
            sys.exit(1)
        except TerraformException as e:
            cprint(e, "red")
            cprint("[ERROR] Terraform execution failed.", "red")
            sys.exit(1)
        except AnsibleException as e:
            cprint(e, "red")
            cprint("[ERROR] Provisioning by Ansible failed.", "red")
            sys.exit(1)

    
    @classmethod
    def scale(
        cls,
        cluster_name: str,
        worker_node: int=None,
    ):
        try:
            cli_scale_input = CLIScaleInput(
                cluster_name = cluster_name,
                worker_node = worker_node
            )
            scale_input = ScaleInput(**cli_scale_input.dict_all())

            if cli_scale_input.scale_type() == "in":
                ScaleIn(scale_input).run()
            elif cli_scale_input.scale_type() == "out":
                ScaleOut(scale_input).run()

        except ValidationError as e:
            cprint("[ERROR] Input value is not correct.", "red")
            validation_result = json.loads(e.json())
            cprint(ValidationFormatter.format(validation_result), "red")
            sys.exit(1)
        except (CheckDeniedException, TerraformStateNotFound) as e:
            cprint(e, "red")
            sys.exit(1)
        except TerraformException as e:
            cprint(e, "red")
            cprint("[ERROR] Terraform execution failed.", "red")
            sys.exit(1)
        except AnsibleException as e:
            cprint(e, "red")
            cprint("[ERROR] Provisioning by Ansible failed.", "red")
            sys.exit(1)
            
    @classmethod
    def delete(
        cls,
        cluster_name: str,
        approve: bool = False
    ):
        try:
            cli_delete_input = CLIDeleteInput(
                cluster_name = cluster_name,
                approve = approve
            )
            delete_input = DeleteInput(**cli_delete_input.dict())
            Delete(delete_input).run()

        except ValidationError as e:
            cprint("[ERROR] Input value is not correct.", "red")
            validation_result = json.loads(e.json())
            cprint(ValidationFormatter.format(validation_result), "red")
            sys.exit(1)
        except CheckDeniedException as e:
            cprint(e, "red")
            sys.exit(1)
        except TerraformException as e:
            cprint(e, "red")
            cprint("[ERROR] Terraform execution failed.", "red")
            sys.exit(1)
