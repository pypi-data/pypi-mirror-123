import os
from pathlib import Path
from typing import List


class Settings:
    # Kubespray related
    KUBESPRAY_VERSION = "2.16.0"
    KUBESPRAY_ARCHIVE_URL = f"https://github.com/kubernetes-sigs/kubespray/archive/refs/tags/v{KUBESPRAY_VERSION}.tar.gz"

    # AWS related
    DEFAULT_AMI: str = "ami-0c3fd0f5d33134a76"
    DEFAULT_INSTANCE_TYPE: str = "t3.medium"
    DEFAULT_AVAILABILITY_ZONE: str = "us-west-1a"
    DEFAULT_CONTROL_PLANE_NUM: int = 1
    DEFAULT_WORKER_NODE_NUM: int = 1
    DEFAULT_OPEN_PORTS: List[int] = [-1]

    # Directory names
    TERRAFORM_TEMPLATE_DIR_NAME: str = "terraform_template"
    ANSIBLE_TEMPLATE_DIR_NAME: str = "ansible_template"
    KUBERNETES_SAMPLE_DIR_NAME: str = "kubernetes_sample"
    DATA_DIR_NAME: str = "data"
    
    # File names
    INVENTORY_FILE_NAME: str = "inventory.yml"
    SETUP_PLAYBOOK_NAME: str = "setup.yml"
    FETCH_ADMIN_CONF_NAME: str = "fetch_admin_conf.yml"
    DISTRO_INFO_FILE_NAME: str = "distro_info.json"
    NODE_INFO_FILE_NAME: str = "node_info.txt.j2"
    VALIDATION_RESULT_FILE_NAME: str = "validation_result.txt.j2"

    # Directory paths
    SELF_PATH: Path = Path(os.path.dirname(__file__)) # Absolute path of the directory where this file belongs to
    TERRAFORM_TEMPLATE_DIR_PATH: Path = SELF_PATH / TERRAFORM_TEMPLATE_DIR_NAME
    ANSIBLE_TEMPLATE_DIR_PATH: Path = SELF_PATH / ANSIBLE_TEMPLATE_DIR_NAME
    KUBERNETES_SAMPLE_DIR_PATH: Path = SELF_PATH / KUBERNETES_SAMPLE_DIR_NAME
    DATA_DIR_PATH: Path = SELF_PATH / DATA_DIR_NAME

    # File paths
    INVENTORY_FILE_PATH: Path = ANSIBLE_TEMPLATE_DIR_PATH / INVENTORY_FILE_NAME
    SETUP_PLAYBOOK_PATH: Path = ANSIBLE_TEMPLATE_DIR_PATH / SETUP_PLAYBOOK_NAME
    FETCH_ADMIN_CONF_PATH: Path = ANSIBLE_TEMPLATE_DIR_PATH / FETCH_ADMIN_CONF_NAME
    DISTRO_INFO_FILE_PATH: Path = DATA_DIR_PATH / DISTRO_INFO_FILE_NAME
    NODE_INFO_FILE_PATH: Path = DATA_DIR_PATH / NODE_INFO_FILE_NAME
    VALIDATION_RESULT_FILE_PATH: Path = DATA_DIR_PATH / VALIDATION_RESULT_FILE_NAME



class ArtifactSettings:

    # Directory names (Artifact)
    KUBESPRAY_ARCHIVE_NAME: str = f"v{Settings.KUBESPRAY_VERSION}.tar.gz"
    KUBESPRAY_DIR_NAME: str = f"kubespray-{Settings.KUBESPRAY_VERSION}"
    RENDERED_TERRAFORM_DIR_NAME: str = "terraform"
    RENDERED_ANSIBLE_DIR_NAME: str = "ansible"
    RENDERED_KUBERNETES_DIR_NAME: str = "kubernetes"
    RENDERED_INVENTORY_NAME: str = "inventory.yml"
    RENDERED_NODE_INFO_NAME: str = "node_info.txt"
    INPUT_JSON_FILE_NAME: str = "input.json"

    def __init__(self, cluster_name: str):
        # Directory paths (Artifact)
        self.ARTIFACT_DIR_PATH: Path = Path.cwd() / cluster_name.replace('-', '_')
        self.KUBESPRAY_ARCHIVE_PATH: Path = self.ARTIFACT_DIR_PATH / self.KUBESPRAY_ARCHIVE_NAME
        self.KUBESPRAY_DIR_PATH: Path = self.ARTIFACT_DIR_PATH / self.KUBESPRAY_DIR_NAME
        self.KUBESPRAY_GROUP_VARS_DIR_PATH: Path = self.KUBESPRAY_DIR_PATH / "inventory/sample/group_vars"
        self.RENDERED_TERRAFORM_DIR_PATH: Path = self.ARTIFACT_DIR_PATH / self.RENDERED_TERRAFORM_DIR_NAME
        self.RENDERED_ANSIBLE_DIR_PATH: Path = self.ARTIFACT_DIR_PATH / self.RENDERED_ANSIBLE_DIR_NAME
        self.RENDERED_KUBERNETES_DIR_PATH: Path = self.ARTIFACT_DIR_PATH / self.RENDERED_KUBERNETES_DIR_NAME
        self.RENDERED_TFSTATE_PATH: Path = self.RENDERED_TERRAFORM_DIR_PATH / "terraform.tfstate"
        self.RENDERED_INVENTORY_PATH: Path = self.RENDERED_ANSIBLE_DIR_PATH / self.RENDERED_INVENTORY_NAME
        self.RENDERED_KUBESPRAY_GROUP_VARS_DIR_PATH: Path = self.RENDERED_ANSIBLE_DIR_PATH / "group_vars"
        self.RENDERED_NODE_INFO_PATH: Path = self.ARTIFACT_DIR_PATH / self.RENDERED_NODE_INFO_NAME
        self.ADMIN_CONF_PATH: Path = self.ARTIFACT_DIR_PATH / "admin.conf"
        self.INPUT_JSON_FILE_PATH: Path = self.ARTIFACT_DIR_PATH / self.INPUT_JSON_FILE_NAME
