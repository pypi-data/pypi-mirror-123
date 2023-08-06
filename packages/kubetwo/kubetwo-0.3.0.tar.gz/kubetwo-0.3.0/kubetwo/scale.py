import json
from typing import List

from kubetwo.model import CreateInput ,ScaleInput
from kubetwo.config import ArtifactSettings
from kubetwo.ansible import Ansible
from kubetwo.common import Common
from kubetwo.terraform import Terraform


class Scale:

    def __init__(self, input: ScaleInput):
        self.input = input
        self.artifact = ArtifactSettings(self.input.cluster_name)

    def post_action(self):
        Common.create_node_info(
            self.artifact.RENDERED_TFSTATE_PATH,
            self.artifact.RENDERED_NODE_INFO_PATH
        )
        Common.save_input_info(
            self.artifact.INPUT_JSON_FILE_PATH, 
            CreateInput(**self.input.dict())
        )


class ScaleIn(Scale):
    
    def run(self):
        terraform = Terraform(self.input.cluster_name)
        terraform.create_terraform_manifests(**self.input.dict())
        terraform.show_plan()
        if not self.input.approve:
            terraform.check_tf_plan()
        
        ansible = Ansible(
            self.input.cluster_name,
            Common.get_default_user_name(self.artifact.RENDERED_TFSTATE_PATH)
        )
        ansible.run_kubespray_scale_in(self.get_remove_nodes())

        terraform.apply()
        ansible.create_inventory_file()

        self.post_action()

    def get_remove_nodes(self) -> List[str]:
        with open(self.artifact.INPUT_JSON_FILE_PATH, "r") as f:
            current_worker_node_num = json.load(f)["worker_node"]
        future_worker_node_num = self.input.worker_node

        remove_nodes = []
        for i in range(current_worker_node_num - future_worker_node_num):
            remove_nodes.append(f"worker-node{current_worker_node_num - i - 1}")
        return remove_nodes


class ScaleOut(Scale):
    
    def run(self):
        terraform = Terraform(self.input.cluster_name)
        terraform.create_terraform_manifests(**self.input.dict())
        terraform.show_plan()
        if not self.input.approve:
            terraform.check_tf_plan()
        terraform.apply()

        ansible = Ansible(
            self.input.cluster_name,
            Common.get_default_user_name(self.artifact.RENDERED_TFSTATE_PATH)
        )
        ansible.create_inventory_file()
        ansible.run_kubespray_scale_out()
        self.post_action()
