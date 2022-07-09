#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Lucas Held <lucasheld@hotmail.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r'''
---
extends_documentation_fragment:
  - lucasheld.uptime_kuma.uptime_kuma

module: tag_info
version_added: 0.0.0
author: Lucas Held (@lucasheld)
short_description: TODO
description: TODO

options:
  id:
    description: The tag id.
    type: int
  name:
    description: The tag name.
    type: str
'''

EXAMPLES = r'''
- name: list tags
  lucasheld.uptime_kuma.tag_info:
    api_url: http://192.168.1.10:3001
    api_username: admin
    api_password: secret
  register: result
'''

RETURN = r'''
'''

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lucasheld.uptime_kuma.plugins.module_utils.common import common_module_args, get_tag_by_name
from ansible.module_utils.basic import missing_required_lib

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    id_ = params.get("id")
    name = params.get("name")

    if id_:
        tag = api.get_tag(id_)
        result["tags"] = [tag]
    elif name:
        tag = get_tag_by_name(api, name)
        result["tags"] = [tag]
    else:
        result["tags"] = api.get_tags()


def main():
    module_args = dict(
        id=dict(type="int"),
        name=dict(type="str"),
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args, supports_check_mode=True)
    params = module.params

    if not HAS_UPTIME_KUMA_API:
        module.fail_json(msg=missing_required_lib("uptime_kuma_api"))

    api = UptimeKumaApi(params["api_url"])
    api.login(params["api_username"], params["api_password"])

    result = {
        "changed": False
    }

    try:
        run(api, params, result)

        api.disconnect()
        module.exit_json(**result)
    except Exception as e:
        api.disconnect()
        error = traceback.format_exc()
        module.fail_json(msg=error, **result)


if __name__ == '__main__':
    main()
