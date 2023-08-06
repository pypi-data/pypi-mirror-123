from pathlib import Path
import shutil
from typing import Dict, List

import ruamel.yaml
from termcolor import cprint

from kubetwo.config import ArtifactSettings, Settings
from kubetwo.common import Common
from kubetwo.exception import *


class Ansible:

    def __init__(self, 
        cluster_name: str,
        user_name: str
    ):
        self.cluster_name = cluster_name
        self.user_name = user_name
        self.ssh_private_key_path = Common.get_ssh_private_key_path()
        self.artifact = ArtifactSettings(cluster_name)
    
    def run_kubespray_create(self):
        command = f"""
            ansible-playbook
            --inventory {str(self.artifact.RENDERED_INVENTORY_PATH)}
            --user {self.user_name}
            --private-key {str(self.ssh_private_key_path)}
            --become
            --become-user=root
            cluster.yml
        """
        command = self._format_command(command)
        try:
            cprint("Creating Kubernetes cluster...")
            Common.run_command(command, cwd=str(self.artifact.KUBESPRAY_DIR_PATH))
            cprint("Finished to create Kubernetes cluster.\n")
        except ProcessException as e:
            raise AnsibleKubesprayException(str(e))

    def run_kubespray_scale_in(self, remove_nodes: List[str]):
        remove_nodes = ",".join(remove_nodes)
        command = f"""
            ansible-playbook
            --inventory {str(self.artifact.RENDERED_INVENTORY_PATH)}
            --user {self.user_name}
            --private-key {str(self.ssh_private_key_path)}
            --become
            --become-user=root
            --extra-vars "node={remove_nodes}" 
            --extra-vars "delete_nodes_confirmation=yes"
            remove-node.yml
        """
        command = self._format_command(command)
        try:
            cprint("Scaling in Kubernetes cluster...")
            Common.run_command(command, cwd=str(self.artifact.KUBESPRAY_DIR_PATH))
            cprint("Finished to scale in Kubernetes cluster.\n")
        except ProcessException as e:
            raise AnsibleKubesprayException(str(e))

    def run_kubespray_scale_out(self):
        command = f"""
            ansible-playbook
            --inventory {str(self.artifact.RENDERED_INVENTORY_PATH)}
            --user {self.user_name}
            --private-key {str(self.ssh_private_key_path)}
            --become
            --become-user=root
            scale.yml
        """
        command = self._format_command(command)
        try:
            cprint("Scaling out Kubernetes cluster...")
            Common.run_command(command, cwd=str(self.artifact.KUBESPRAY_DIR_PATH))
            cprint("Finished to scale out Kubernetes cluster.\n")
        except ProcessException as e:
            raise AnsibleKubesprayException(str(e))

    def run_setup(self):
        playbook_dir_path = Settings.ANSIBLE_TEMPLATE_DIR_PATH
        command = f"""
            ansible-playbook
            --inventory {str(self.artifact.RENDERED_INVENTORY_PATH)}
            --user {self.user_name}
            --private-key {str(self.ssh_private_key_path)}
            {Settings.SETUP_PLAYBOOK_NAME}
        """
        command = self._format_command(command)
        try:
            cprint("Setting up Kubernetes cluster...")
            Common.run_command(command, cwd=str(playbook_dir_path))
            cprint("Finished to set up Kubernetes cluster.\n")
        except ProcessException as e:
            raise AnsibleSetupException(str(e))

    def run_fetch_admin_conf(
        self, 
        artifact_dir_path: Path,
        admin_conf_path: Path,
        first_control_plane: Dict
    ):
        playbook_dir_path = Settings.ANSIBLE_TEMPLATE_DIR_PATH
        command = f"""
            ansible-playbook
            --inventory {str(self.artifact.RENDERED_INVENTORY_PATH)}
            --user {self.user_name}
            --private-key {str(self.ssh_private_key_path)}
            --extra-vars dest_path={str(artifact_dir_path)}
            {Settings.FETCH_ADMIN_CONF_NAME}
        """
        command = self._format_command(command)
        try:
            cprint("Fetching admin.conf from control plane...")
            Common.run_command(command, cwd=str(playbook_dir_path))
            self._render_admin_conf(
                artifact_dir_path,
                admin_conf_path,
                first_control_plane,
            )
            cprint("Finished to fetch admin.conf from control plane.\n")
        except ProcessException as e:
            raise AnsibleFetchAdminConfException(str(e))

    def create_inventory_file(self):
        cprint("Rendering inventory file for Ansible...")
        yaml = ruamel.yaml.YAML()
        control_plane_list, worker_node_list = Common.get_node_info(self.artifact.RENDERED_TFSTATE_PATH)

        if len(control_plane_list) % 2 == 0:
            etcd_count = len(control_plane_list) - 1
        else:
            etcd_count = len(control_plane_list)

        with open(Settings.INVENTORY_FILE_PATH, "r") as stream:
            inventory = yaml.load(stream)

        for node in control_plane_list + worker_node_list:
            inventory["all"]["hosts"][node["name"]] = {
                "ansible_ssh_host": node["public_ip"],
                "ip": node["private_ip"],
                "access_ip": node["private_ip"]
            }

        for control_plane in control_plane_list:
            inventory["all"]["children"]["kube_control_plane"]["hosts"][control_plane["name"]] = None

        for worker_node in worker_node_list:
            inventory["all"]["children"]["kube_node"]["hosts"][worker_node["name"]] = None

        for control_plane in control_plane_list[:etcd_count]:
            inventory["all"]["children"]["etcd"]["hosts"][control_plane["name"]] = None

        with open(self.artifact.RENDERED_INVENTORY_PATH, "w") as stream:
            yaml.dump(inventory, stream=stream)

        cprint(f"Finished to render inventory file ({self.artifact.RENDERED_INVENTORY_PATH}).\n")

    def copy_group_vars(self):
        yaml = ruamel.yaml.YAML()
        src = str(self.artifact.KUBESPRAY_GROUP_VARS_DIR_PATH)
        dest = str(self.artifact.RENDERED_KUBESPRAY_GROUP_VARS_DIR_PATH)
        shutil.copytree(src, dest)

        for path in self.artifact.RENDERED_ANSIBLE_DIR_PATH.glob('**/*.yml'):
            if path.name == "inventory.yml":
                continue
            with open(path, "r") as stream:
                group_vars = yaml.load(stream)
            
            if path.name == "k8s-cluster.yml":
                group_vars["cluster_name"] = self.cluster_name
            
            if path.name == "addons.yml":
                group_vars["helm_enabled"] = True

            with open(path, "w") as stream:
                yaml.dump(group_vars, stream=stream)

    def _render_admin_conf(
        self, 
        artifact_dir_path: Path,
        admin_conf_path: Path,
        first_control_plane: Dict
    ):
        yaml = ruamel.yaml.YAML()
        admin_conf_src_path = artifact_dir_path / f"{first_control_plane['name']}/admin.conf"
        with open(admin_conf_src_path, "r") as stream:
            admin_conf = yaml.load(stream)

        clusters = []
        for cluster in admin_conf["clusters"]:
            cluster_info = cluster["cluster"]
            cluster_info.pop("certificate-authority-data", None)
            cluster_info["insecure-skip-tls-verify"] = True
            cluster_info["server"] = f"https://{first_control_plane['public_ip']}:6443"
            cluster["cluster"] = cluster_info
            clusters.append(cluster)
        admin_conf["clusters"] = clusters

        with open(admin_conf_path, "w") as stream:
            yaml.dump(admin_conf, stream=stream)

        shutil.rmtree(str(artifact_dir_path / f"{first_control_plane['name']}"))

    def _format_command(self, command: str) -> str:
        command = command.replace("\n", " ")
        command = " ".join(command.split())
        return command
