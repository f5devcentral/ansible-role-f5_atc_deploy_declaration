#!/usr/bin/python
import os
import json
from ansible.module_utils.basic import AnsibleModule


def process_json(data, ansible_version):
    try:
        assert data["class"]
        assert data["class"].lower() == "as3"
        assert data["declaration"]
        assert data["declaration"]["class"].lower() == "adc"
        if "controls" in data["declaration"]:
            assert not data["declaration"]["controls"]["userAgent"]
    except AssertionError:
        return (False, None)

    as3_declaration = data["declaration"]

    if "controls" not in as3_declaration:
        adc_controls = {
            "class": "Controls",
            "userAgent": "ansible/{ansible_version}".format(
                ansible_version=ansible_version)
        }
        data["declaration"]["controls"] = adc_controls
    else:
        data["declaration"]["controls"]["userAgent"] = \
            "ansible/{ansible_version}".format(
                ansible_version=ansible_version)
    return (True, data)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            json_file_path=dict(required=True)
        ),
        supports_check_mode=True,
    )

    json_file_path = module.params['json_file_path']

    json_file_object = open(json_file_path, 'r')
    data = json.load(json_file_object)
    json_file_object.close()

    (isChanged, result) = process_json(data, module.ansible_version)

    results = dict(
        changed=isChanged,
        result=result
    )

    if isChanged and result is not None:
        json_file_object = open(json_file_path, 'w')
        json.dump(result, json_file_object, indent=4)
        json_file_object.close()

    module.exit_json(**results)


if __name__ == '__main__':
    main()
