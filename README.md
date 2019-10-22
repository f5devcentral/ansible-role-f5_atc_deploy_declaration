# Ansible Role: F5 automation tool chain (ACT) deploy declaration

Deploys declaritives to automation tool chain services (AS3, DO, TS).

## Requirements

Corrisponding ACT service must be installed on BIG-IP or BIG-IQ prior to deploying declaration.

## Role Variables

Available variables are listed below. For their default values, see `defaults/main.yml`:

    act_server: "{{ ansible_host }}"
    act_port: 443
    act_user:
    act_password:
    act_validate_certs: true
    act_transport: rest
    act_timeout: 120

Establishes initial connection to your BIG-IQ. These values are substituted into
your ``provider`` module parameter.

Required

    act_method: POST

act_method accepted values include [POST, GET] for all services, and [DELETE] for AS3 only.
f5_act_deply_declaration role currently does not support AS3 PATCH method.

Required

    act_declaration_file:

Local location of declaration.

Required.

    act_declaration_url:

URL of declaration location

Optional

File at url specfied is downloaded to path/filename specified in varable act_declaration_file.

Default is null.

    as3_tenant:

POSTing to a specific AS3 tenant.

Optional

Starting with AS3 3.14.0, you have the option of using POST to the /declare endpoint
with a specific tenant in the URI (for example …/declare/tenant1). This only updates
the tenant you specified, even if there are other tenants in the declaration. This
can be useful in some automation scenarios involving AS3.

For example, when POSTING to the URI /mgmt/shared/appsvcs/declare/tenant1,tenant2:

If both tenant1 and tenant2 are in the declaration you are posting, both tenants are
updated and AS3 returns both tenants in the response.

If only tenant1 is present in the declaration you are posting, only tenant1 is updated
and returned in the response, despite the fact tenant2 is included in the URI.

If the tenant in the URI and the tenant in the declaration do not match (for example, only
tenant3 is present in the declaration), AS3 returns a “no change” response.

Default is null.

    as3_show: base

You can use the following URL query parameters for POST, GET, or DELETE
Required
``base means`` system returns the declaration as originally deployed (but with secrets
like passphrases encrypted), full returns the declaration with all default schema
properties populated, expanded includes all URLs, base64s, and other references expanded
to their final static values.

Acceptable values include: base, full, expanded
Default is base

    as3_showhash: true

You can use the following URL query parameters for POST (Note: showHash for POST was
introduced in AS3 3.14.0 and will only work on 3.14.0 and later):

This was introduced as a protection mechanism for tenants in a declaration
(previously you had to use a separate GET request to retrieve the Optimistic lock).
If you set “showHash=true”, the results include an optimisticLockKey for each tenant.
Attempts to change/update any of the tenants without the correct optimisticLockKey will fail.

Optional

Default is false.

    as3_async: false

Async with AS3 3.5.0+

Optional

Setting async to true causes AS3 to respond with a 202 status and a request ID which
you can later use in a GET request to a new /task endpoint to get the results. Typically
only used with extremely large declarations which take a long time for AS3 to process.
The record IDs expire after 24 hours. When you retrieve a record, AS3 deletes the record
along with any expired records. A GET to /task with no record ID specified returns
(and deletes) all records.

Default is false.



## Dependencies

None.

## Example Playbook

    - name: Deploy AS3 Declaration
      hosts: bigip
      vars_files:
        - vars/main.yml
      roles:
        - { role: f5devcentral.f5_act_deploy_declaration }

*Inside `vars/main.yml`*:

    act_server: "{{ ansible_host }}"
    act_port: 443
    act_user: admin
    act_password: admin
    act_validate_certs: true
    act_transport: rest
    act_timeout: 120
    act_method: POST
    act_declaration_file: files/example_as3_declaration.json
    act_declaration_url: https://raw.githubusercontent.com/crosbygw/declaritives/master/files/example_as3_declaration.json
    as3_tenant: Sample_01
    as3_show: base
    as3_showhash: true
    as3_async: false

## License

Apache

## Author Information

This role was created in 2019 by [Greg Crosby](https://github.com/crosbygw).<br>
