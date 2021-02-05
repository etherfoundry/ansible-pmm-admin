#!/usr/bin/python

DOCUMENTATION = """
---
module: pmm_admin
short_description: Use pmm-admin to add DB instances to PMM2
"""

DOCUMENTATION = """
---
module: pmm_admin

short_description: Use pmm-admin to add DB instances to PMM2

version_added: "2.9.10"

description:
    - "A module used to add/remove instances to a PMM2 instance"

options:
    state:
        description:
            - Desired state of the item (present|absent)
        required: true
    database:
        description:
            - What kind of DB to connect to (mysql|mongodb|postgresql|proxysql)
        required: true
    username:
        description:
            - Username to use when connecting
        required: false
    password:
        description:
            - Password to authenticate to DB
        required: false
    hostname:
        description:
            - DB hostname
        required: false
    environment:
        description:
            -  Environment name
        required: false
    cluster:
        description:
            - Cluster name
        required: false
    replication_set:
        description:
            - Replication set
        required: false
    tls:
        description:
            - Use TLS (true|false)
        required: false


author:
    - Alexandros Orfanos (@aorfanos)
"""

EXAMPLES = """
- name: Create a Grafana annotation
  add_grafana_annotation:
    grafana_api_url: "https://grafana.myproject.com"
    grafana_api_key: "..."
    dashboard_id: 468
    panel_id: 20
    text: "Annotation description"
    tags:
      - tag1
      - tag2
  register: result
"""

RETURN = """
remote_status_code:
    description: The HTTP return code of the RESTFul call to Grafana API
    type: int
message:
    description: An auxiliary message, containing the return code and (very) basic troubleshooting info
"""

ANSIBLE_METADATA = {
    "status": ["preview"],
    "supported_by": "community",
    "metadata_version": "1.0",
}

from ansible.module_utils.basic import AnsibleModule
import subprocess
import requests
import json
import urllib.request as urllib


def get_dashboard_by_name(dashboardName, grafanaApiUrl, authHeaders):
    _url = "{}/api/search?query={}".format(
        grafanaApiUrl, urllib.quote(dashboardName, safe="")
    )
    result = requests.get(_url, headers=authHeaders).json()
    for res in result:
        return res["id"]


def run_module():

    module_args = dict(
        database=dict(type="str", required=True),
        hostname=dict(type="str", required=True),
        username=dict(type="str", required=False, no_log=True),
        password=dict(type="str", required=False, no_log=True),
        environment=dict(type="str", required=False),
        tls=dict(type="bool", required=False, default=False),
        state=dict(type="str", required=True),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    cmd = [
        "pmm-admin",
        "add",
        str(module.params["database"]),
    ]

    if module.params["username"] is not None:
        cmd.append("--username='{}'".format(module.params["username"]))
    if module.params["password"] is not None:
        cmd.append("--password='{}'".format(module.params["password"]))
    if module.params["hostname"] is not None:
        cmd.append("{}".format(module.params["hostname"]))
    if module.params["environment"] is not None:
        cmd.append("--environment={}".format(module.params["environment"]))
    if module.params["tls"] is not None:
        cmd.append("--tls='{}'".format(module.params["tls"]))

    result = dict(changed=False, stdout=cmd)

    # _database = input("Database type: ")
    # _username = input("Add a username: ")
    # _password = input("Add a password: ")
    # _hostname = input("Add hostname: ")
    # _optional = input("Add an optional arg: ")

    # cmd = [
    #     "pmm-admin",
    #     "add",
    #     str(_database),
    #     ]

    # if _username is not None: cmd.append("--username='{}'".format(_username))
    # if _password is not None: cmd.append("--password='{}'".format(_password))
    # if _hostname is not None: cmd.append("--hostname='{}'".format(_hostname))
    # if _optional is not None: cmd.append("--tls='{}'".format(_optional))

    # print(cmd)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
