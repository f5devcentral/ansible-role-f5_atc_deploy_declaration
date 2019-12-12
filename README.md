# Ansible Role: F5 automation tool chain (ATC) deploy declaration

This role deploys declaratives to installed automation tool chain services (AS3, DO, TS) on your BIG-IP or BIG-IQ. You would use this role to post declarations to the following BIG-IP or BIG-IQ automation tool chain services: application services 3 extension, declaritive onboarding, or telemetry streaming. Information regarding these services along with example declaritives is available on [f5-cloud-docs](https://clouddocs.f5.com/).

* note: this role determines which service to use by the referenced declarative which should contain the service class.
For example, AS3 declaratives will contain a service pointer using key "class": with value "AS3" in json declared file [Example](https://clouddocs.f5.com/products/extensions/f5-appsvcs-extension/latest/declarations/http-services.html#http-with-custom-persistence). Be sure to define service pointers at the beginning of your declaration.

## Requirements

Corresponding ATC service must be installed on BIG-IP or BIG-IQ prior to deploying declaration.

## Role Variables

Available variables are listed below. For their default values, see `defaults/main.yml`:

    provider:
      server: "{{ atc_server }}"
      server_port: "{{ atc_port }}"
      user: "{{ atc_user }}"
      password: "{{ atc_password }}"
      validate_certs: "{{ atc_validate_certs }}"
      transport: "{{ atc_transport }}"
      provider: "{{ atc_provider}}"

Establishes initial connection to your BIG-IQ or BIG-IP. These values are substituted into
your ``provider`` module parameter.

Required

    atc_method: GET

atc_method accepted values include [POST, GET] for all services, and [DELETE] for AS3 only.
f5_atc_deploy_declaration role currently does not support AS3 PATCH method.

Required

    atc_declaration_file:

Local location of declaration, only required if `atc_service` is not provided

Required

    atc_declaration_url:

URL of declaration location

Optional.

    atc_service:
    
Required if `atc_declaration_file` is not present and the requested `atc_method` is `GET`.


Optional

File at url specfied is downloaded to path/filename specified in variable `atc_declaration_file`.

Default is null.

    atc_delay: 30

Amount of time between retires when checking service status

Required

Default 30 seconds

    atc_retries: 10

Number of times to retry service status

Required

Default 10

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



## Dependencies

None.

## Example Playbook

    - name: Deploy AS3 Declaration
      hosts: bigip
      vars_files:
        - vars/main.yml
      vars:
        provider:
          server: "{{ atc_server }}"
          server_port: "{{ atc_port }}"
          user: "{{ atc_user }}"
          password: "{{ atc_password }}"
          validate_certs: "{{ atc_validate_certs }}"
          transport: "{{ atc_transport }}"  
      roles:
        - { role: f5devcentral.f5_atc_deploy_declaration }

*Inside `vars/main.yml`*:

    atc_server: "{{ ansible_host }}"
    atc_port: 443
    atc_user: admin
    atc_password: admin
    atc_validate_certs: true
    atc_transport: rest
    atc_timeout: 120
    atc_method: POST
    atc_declaration_file: files/example_as3_declaration.json
    atc_declaration_url: https://raw.githubusercontent.com/f5devcentral/ansible-role-f5_atc_deploy_declaration/master/files/example_as3_declaration.json
    atc_delay: 30
    atc_retries: 10
    as3_tenant: Sample_01
    as3_show: base
    as3_showhash: true
    as3_async: false

## License

Apache

## Author Information

This role was created in 2019 by [Greg Crosby](https://github.com/crosbygw).<br>

## Credits

A special thanks to Vinnie Mazza ([@vinnie357](https://github.com/vinnie357)) for the
ansible playbook examples.
