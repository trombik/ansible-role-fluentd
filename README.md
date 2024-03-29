# ansible-role-fluentd

Configures `fluentd`.

## Notes for FreeBSD

The
[`sysutils/rubygem-fluentd`](https://www.freshports.org/sysutils/rubygem-fluentd/)
port does not patch the gem to include `fluentd_plugin_dir`, or
`/usr/local/etc/fluentd/plugin`, by default (as of version `0.12.14_1`). If you
manage local plugins in the directory, you need to set `fluentd_flags`.

```yaml
fluentd_flags: "-p {{ fluentd_plugin_dir }}"
```

See [Add a Plugin Via
/etc/fluent/plugin](http://docs.fluentd.org/v0.12/articles/plugin-management#add-a-plugin-via-etcfluentplugin)
for more details.

Note that `fluentd_plugins_to_install`  does not use `fluentd_plugin_dir`.

# Requirements

This role requires the following `ansible` collections:

* community.general

# Role Variables

| variable | description | default |
|----------|-------------|---------|
| `fluentd_user`                | the user of `fluentd` | `{{ __fluentd_user }}` |
| `fluentd_group`               | the group of `fluentd` | `{{ __fluentd_group }}` |
| `fluentd_extra_groups` | list of extra group names (preferred) or a comma-separated string of group names (deprecated, for backward-compatibility) that `fluentd` user belongs to | `[]` |
| `fluentd_package_name`        | package name of `fluentd` | `{{ __fluentd_package_name }}` |
| `fluentd_config_dir`          | path to config directory | `{{ __fluentd_config_dir }}` |
| `fluentd_config_file`         | path to `fluent.conf` | `{{ __fluentd_config_file }}` |
| `fluentd_config_fragment_dir` | path to `conf.d` directory | `{{ fluentd_config_dir }}/conf.d` |
| `fluentd_service_name`        | service name of `fluentd` | `{{  __fluentd_service_name }}` |
| `fluentd_plugin_dir`          | path to directory where local plugins reside | `{{ fluentd_config_dir }}/plugin` |
| `fluentd_flags`               | flags for the service | `{{ __fluentd_flags }}` |
| `fluentd_gem_bin`             | path to `fluent-gem`  | `{{ __fluentd_gem_bin }}` |
| `fluentd_plugins_to_install`  | list of plug-in names to install | `[]` |
| `fluentd_plugins_to_create`   | list of plug-ins to _create_ (see below) | `[]` |
| `fluentd_gems`                | a list of dict of to manage gems | `[]` |
| `fluentd_certs_dir`           | path to directory where cert files reside | `{{ __fluentd_config_dir }}/certs` |
| `fluentd_configs`             | dict of config fragments, see below | {} |
| `fluentd_ca_key`              | content of `ca_key.pem` | "" |
| `fluentd_ca_cert`             | content of `ca_cert.pem` | "" |
| `fluentd_ca_private_key_passphrase` | the passphrase of `ca_key.pem` | "" |
| `fluentd_buffer_path`         | path to file-based buffer directory | `/var/spool/fluentd` |
| `fluentd_unix_pipe_dir`       | path to directory where `AF_UNIX` pipe should be created | `{{ __fluentd_unix_pipe_dir }}` |
| `fluentd_log_dir`             | path to directory where `fluentd` *can* write logs. Set `None` to disable | `/var/log/{{ fluentd_service_name }}` |
| `fluentd_log_file` | path to log file | `{{ fluentd_log_dir }}/{{ fluentd_service_name }}.log` |
| `fluentd_system_config`       | a string that is enclosed by `<system>` tag in `fluentd.conf`. use `|` in yaml to set multiple lines of system-wide configurations | `log_level error` |
| `fluentd_pid_dir` | path to PID directory | `"{{ __fluentd_pid_dir }}"` |
| `fluentd_pid_file` | path to PID file | `"{{ __fluentd_pid_file }}"` |
| `fluentd_extra_files` | list of extra files to create or delete (see below) | `[]` |
| `fluentd_extra_packages` | list of extra packages to install | `[]` |

Note that although the role provides `fluentd_log_dir` and `fluentd_log_file`,
you need to configure `fluentd` to log to `fluentd_log_file`. The role does
_NOT_ configures `fluentd` to log to the file. See Example Playbook for how.

## `fluentd_plugins_to_create`

This variable is list of dict. The dict is described below. The role creates
plug-ins listed in this variable under `fluentd_plugin_dir`.

| Key | Description | Mandatory? |
|-----|-------------|------------|
| name | file name of the plug-in | yes |
| content | content of the plug-in, must be valid ruby code | yes |
| state | state of the plug-in, either `present` or `absent` | yes |

## `fluentd_configs`

Key is the name of the config fragment file. the key has a hash described
below. The role creates a configuration fragment of `config` under
`fluentd_config_fragment_dir`.

| key     | value                                            |
|---------|--------------------------------------------------|
| enabled | bool, create the config if true, remove if false |
| config  | the configuration                                |

## `fluentd_extra_files`

This variable is a list of dict that represent files to create or delete.
Useful for files that is not part of `fluentd` configuration, such as a
`elasticsearch` template. An example use-case is
[`template_file`](https://github.com/uken/fluent-plugin-elasticsearch#template_file)
for `fluent-plugin-elasticsearch`.

| key       | value                                           |
|-----------|-------------------------------------------------|
| `path`    | path to the file                                |
| `state`   | state of the file, either `present` or `absent` |
| `content` | the content of the file                         |
| `owner`   | the owner of the file, optional                 |
| `group`   | the group of the file, optional                 |
| `mode`    | the mode of the file, optional                  |

## `fluentd_gems`

This variable is a list of dict. The dict accepts all keys that
`community.general.gem` accepts. `name` is required. Other keys are omitted if
the key does not exist except the following keys.

* `user_install` defaults to `no`
* `executable` defaults to `fluentd_gem_bin`

## Debian

| Variable | Default |
|----------|---------|
| `__fluentd_user` | `td-agent` |
| `__fluentd_group` | `td-agent` |
| `__fluentd_package_name` | `td-agent` |
| `__fluentd_service_name` | `td-agent` |
| `__fluentd_config_dir` | `/etc/td-agent` |
| `__fluentd_config_file` | `{{ fluentd_config_dir }}/td-agent.conf` |
| `__fluentd_bin` | `/usr/sbin/td-agent` |
| `__fluentd_gem_bin` | `/usr/sbin/td-agent-gem` |
| `__fluentd_unix_pipe_dir` | `/var/tmp/fluentd` |
| `__fluentd_flags` | `""` |
| `__fluentd_pid_dir` | `/var/run/td-agent` |
| `__fluentd_pid_file` | `{{ fluentd_pid_dir }}/td-agent.pid` |

## FreeBSD

| Variable | Default |
|----------|---------|
| `__fluentd_user` | `fluentd` |
| `__fluentd_group` | `fluentd` |
| `__fluentd_package_name` | `rubygem-fluentd` |
| `__fluentd_service_name` | `fluentd` |
| `__fluentd_config_dir` | `/usr/local/etc/fluentd` |
| `__fluentd_config_file` | `{{ fluentd_config_dir }}/fluent.conf` |
| `__fluentd_bin` | `/usr/local/bin/fluentd` |
| `__fluentd_gem_bin` | `/usr/local/bin/fluent-gem` |
| `__fluentd_unix_pipe_dir` | `/var/tmp/fluentd` |
| `__fluentd_flags` | `""` |
| `__fluentd_pid_dir` | `/var/run/fluentd` |
| `__fluentd_pid_file` | `{{ fluentd_pid_dir }}/fluentd.pid` |

## OpenBSD

| Variable | Default |
|----------|---------|
| `__fluentd_user` | `_fluentd` |
| `__fluentd_group` | `_fluentd` |
| `__fluentd_package_name` | `rubygem-fluentd` |
| `__fluentd_service_name` | `fluentd` |
| `__fluentd_config_dir` | `/etc/fluentd` |
| `__fluentd_config_file` | `{{ fluentd_config_dir }}/fluent.conf` |
| `__fluentd_bin` | `/usr/local/bin/fluentd26` |
| `__fluentd_gem_bin` | `/usr/local/bin/fluent-gem` |
| `__fluentd_unix_pipe_dir` | `/var/tmp/fluentd` |
| `__fluentd_flags` | `""` |
| `__fluentd_pid_dir` | `/var/run/fluentd` |
| `__fluentd_pid_file` | `{{ fluentd_pid_dir }}/fluentd.pid` |

## RedHat

| Variable | Default |
|----------|---------|
| `__fluentd_user` | `td-agent` |
| `__fluentd_group` | `td-agent` |
| `__fluentd_package_name` | `td-agent` |
| `__fluentd_service_name` | `td-agent` |
| `__fluentd_config_dir` | `/etc/td-agent` |
| `__fluentd_config_file` | `{{ fluentd_config_dir }}/td-agent.conf` |
| `__fluentd_bin` | `/usr/sbin/td-agent` |
| `__fluentd_gem_bin` | `/usr/sbin/td-agent-gem` |
| `__fluentd_unix_pipe_dir` | `/var/tmp/fluentd` |
| `__fluentd_flags` | `""` |
| `__fluentd_pid_dir` | `/var/run/td-agent` |
| `__fluentd_pid_file` | `{{ fluentd_pid_dir }}/td-agent.pid` |

# Dependencies

- [trombik.language-ruby](https://github.com/trombik/ansible-role-language-ruby) (OpenBSD, Ubuntu, and RedHat)

# Example Playbook

```yaml
---
- hosts: localhost
  roles:
    - name: trombik.apt_repo
      when: ansible_os_family == 'Debian'
    - name: trombik.redhat_repo
      when: ansible_os_family == 'RedHat'
    - name: trombik.language_ruby
    - ansible-role-fluentd
  vars:
    fluentd_extra_files:
      - path: "{{ fluentd_config_dir }}/es_templates/logstash_template.json"
        mode: '0664'
        state: present
        content: |
          {
            "mappings": {
              "_default_": {
                "_all": { "enabled": false },
                "_source": { "compress": true },
                "properties" : {
                  "event_data": { "type": "object", "store": "no" },
                  "@fields": { "type": "object", "dynamic": true, "path": "full" },
                  "@message": { "type": "string", "index": "analyzed" },
                  "@source": { "type": "string", "index": "not_analyzed" },
                  "@source_host": { "type": "string", "index": "not_analyzed" },
                  "@source_path": { "type": "string", "index": "not_analyzed" },
                  "@tags": { "type": "string", "index": "not_analyzed" },
                  "@timestamp": { "type": "date", "index": "not_analyzed" },
                  "@type": { "type": "string", "index": "not_analyzed" }
                }
              }
            },
            "settings": {
              "index.cache.field.type" : "soft",
              "index.refresh_interval": "5s",
              "index.store.compress.stored": true,
              "index.number_of_shards": "3",
              "index.query.default_field": "querystring",
              "index.routing.allocation.total_shards_per_node": "2"
            },
            "template": "logstash-*"
          }
    os_fluentd_extra_packages:
      FreeBSD:
        - net/libmaxminddb
      RedHat: []
      Debian:
        - libmaxminddb-dev
      OpenBSD: []
    fluentd_extra_packages: "{{ os_fluentd_extra_packages[ansible_os_family] }}"

    os_language_ruby_package:
      FreeBSD: lang/ruby27
      OpenBSD: ruby%2.7
      RedHat: "{{ __language_ruby_package }}"
      Debian: "{{ __language_ruby_package }}"
    language_ruby_package: "{{ os_language_ruby_package[ansible_os_family] }}"
    apt_repo_keys_to_add:
      - https://packages.treasuredata.com/GPG-KEY-td-agent
    apt_repo_to_add:
      - "deb http://packages.treasuredata.com/4/ubuntu/{{ ansible_distribution_release }}/ {{ ansible_distribution_release }} contrib"
    redhat_repo:
      treasuredata:
        baseurl: http://packages.treasuredata.com/4/redhat/$releasever/$basearch
        gpgkey: https://packages.treasuredata.com/GPG-KEY-td-agent
    fluentd_extra_groups: tty,bin

    os_fluentd_flags:
      FreeBSD: |
        fluentd_flags="-p {{ fluentd_plugin_dir }} --log {{ fluentd_log_file }}"
      Debian: |
        TD_AGENT_LOG_FILE="{{ fluentd_log_file }}"
        TD_AGENT_OPTIONS="-p {{ fluentd_plugin_dir }}"
        STOPTIMEOUT=180
      RedHat: |
        TD_AGENT_LOG_FILE="{{ fluentd_log_file }}"
        TD_AGENT_OPTIONS=""
      OpenBSD: "--daemon /var/run/fluentd/fluentd.pid --config {{ fluentd_config_file }} -p {{ fluentd_plugin_dir }} --log {{ fluentd_log_file }}"
    fluentd_flags: "{{ os_fluentd_flags[ansible_os_family] }}"
    os_fluentd_bin:
      OpenBSD: "/usr/local/bin/fluentd{{ language_ruby_version['short'] }}"
      FreeBSD: "{{ __fluentd_bin }}"
      RedHat: "{{ __fluentd_bin }}"
      Debian: "{{ __fluentd_bin }}"
    fluentd_bin: "{{ os_fluentd_bin[ansible_os_family] }}"
    fluentd_system_config: |
      log_level debug
      suppress_config_dump
    fluentd_plugins_to_install:
      - fluent-plugin-redis
      - fluent-plugin-secure-forward
    fluentd_plugins_to_create:
      - name: in_example.rb
        content: "{{ lookup('file', 'files/in_example.rb') }}"
        state: present
    fluentd_ca_cert: |
      -----BEGIN CERTIFICATE-----
      MIIDIDCCAggCAQEwDQYJKoZIhvcNAQEFBQAwTTELMAkGA1UEBhMCVVMxCzAJBgNV
      BAgMAkNBMRYwFAYDVQQHDA1Nb3VudGFpbiBWaWV3MRkwFwYDVQQDDBBTZWN1cmVG
      b3J3YXJkIENBMB4XDTcwMDEwMTAwMDAwMFoXDTIxMDQxNTE3MDE1OVowTTELMAkG
      A1UEBhMCVVMxCzAJBgNVBAgMAkNBMRYwFAYDVQQHDA1Nb3VudGFpbiBWaWV3MRkw
      FwYDVQQDDBBTZWN1cmVGb3J3YXJkIENBMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A
      MIIBCgKCAQEAsubDxMCBata8T8++x85nlsEyXT+fEXseZAln+RffZJqqdsJtbLmc
      /a7u40IefQBShm3itba0dMTsPnG8rrvLtkz+3TSuN6wBTR+iM5/vBlu9Z8b983c9
      HZ/RkDzhlucqzDSIstYbpLDefiw78ME2kpzIbDpmsudzYQCK1XHr7eIVog9pSjJS
      UEvj967lFX1T+ajpib/cqOSjjmjCbA91Pdo+il8iTHSo+SFgG3mIVDNnztD9nBUi
      96sWblnEDlzSH8MV9AOwM/FxI2HQ+giNQnc2NXt7q5wHBNG7fQ19+IiQ7tHjyvke
      eQ3POmo00+NSVcKObX29e6PCqiD14OrnLQIDAQABoxAwDjAMBgNVHRMEBTADAQH/
      MA0GCSqGSIb3DQEBBQUAA4IBAQB6t43EHkd2d8P25h1QNE1136VwC+OHg5ThPmXU
      wexuLY35iyWDs8AdZm2wu+9L0TAd3pqqY6qJW5JblTTGFZ3372oe2043EpcGVxxF
      /ov7VtlcD/Govu8IDkKhzojDrcKEoZCaI2zLaJpDZx5O/Zki0+fAOSNA+9HuLxUv
      mzCgQMazeUYkvvqxnm64Skw07xQ/g8JvjmFxfOz1LqMjY/M5TOXHUTZJFwpZVwHD
      8yt/MboSjEItdGb9qQlDfajYNYbodbbhurDXmwXRJU10uUK3RekKWOGKKoRhEOJ1
      SCi2iwz7n1N+bqXB8nLDOOr/zL1a4zev/KpMRhQNYMFswzUe
      -----END CERTIFICATE-----
    fluentd_ca_private_key_passphrase: password
    fluentd_ca_key: |
      -----BEGIN RSA PRIVATE KEY-----
      Proc-Type: 4,ENCRYPTED
      DEK-Info: AES-256-CBC,CB41DBD602640F0131B108162FBDA4C1

      eUVHk/0/haiey+uTvUVjLMG1uKqXEKzqbhuna3k+dPuOTOYPPrAArNfVgXS3K+rV
      kjsJUGLxwseC2Q9krbOx0tHoY25elMMGW/G46tds5CRJ5quoQIFXfuD8TBBSDEAI
      QFlU8PgUx+6KhEy63xjM1c9Y8CsgJqwpxWO6p6lAvJfVvuzUGBdEc7WvkDzmpGZk
      aNggxKJnd1qy/YNe1gbYpXPrn7y001s3CJtKs3goMJ6baMWfaUBDx6EBx7lJgL/r
      MqCWT+3q2McK3HcqEwK2O4oimlJy2pGj/SDESCPRGmKcYz6MLCZMoEjRDRWgZln8
      L9maXurGCIKsiBz61vNFGZtmu/dPJaJISPF3s4RTh7mst4SgWeNWK88dn6XAygkd
      yHOSM0l5y4YEqxiyPof7uAZBd276yMFp0mO8Hf61rtrTmUz/3nE4rsTTmGI60FIk
      PbzxZbWkZRcWNnDJE9ijuoqQ4W1ZGx5YkhNb5Al/Bap2rZ8ksEtpJswkGTm/j16i
      oSDpgu2ArSnxllbd7PWug/suCoullXlOJuOg3U5zrVASdAcUTK5872ObE40LzVPI
      4PRDYmYjvAIml2MjsXM1qlaN/qr8vnoRb+wZB0c3Jqj+eIVSPkypBcRxeeSp8akT
      Sdt7JmROdSgH7Sv9zdgJreMDofkQns6RN3TpEWnnDhZrE1vWQxF2DhNxeGThouqr
      QCdSv2DDPM6PgJEjFSXAYOKdeO+s22kzUv87fI+ubuU8gesSL7uAELSVHaXe/zKw
      9dGWVVIYfZ7F61aBXYqz598N2EqUv2rviQTWeVJ6Xggr/O7s6N7U6rn+1ptFcUTl
      BrPOdQws3Syc2NE2qov1A1QQ2uQQcy0l7bEEOuc1jxLKUMl5+ZWl94iZ5tg+3zG8
      QMf74rel6ELi1zVGcmwAROgt0AlOzQ7X8iiOjM1E9ZkplnQWaXbXRcZKlkYtnVHg
      Vk/bs2Fs2+qHpNR0m4nNzeWxcm5z/wN2xgJFRPyiOJDSMYfwnNPM3TEOg72RUtBi
      PT8Is8vRb7pb6JjT20OScxymNgOFYRAkcKQn2vVrrA7CWJpA7xeNbcoLM99bSOl7
      upgzyIb5jK8NzUwCv1kjCkESO3tGkfHPLbfXFzj966PEsR4Cyr5Mh8MiPk8p9VQV
      of27ZcwGCwiR7spMTKAQWEComDegZoN2pYELJL78Cb36p4mfu6pi9Ka6XeBoO7Hp
      zPFY9HPVjHHUAYZcFvLlMoaZz+VzjeATxAiSmD/iuWu9aJ77653cCzcicUOVM2T2
      nu1mMNm2EcPLXgZ4MqDLcwmYDV+GKdR2ilVdlbjKquf8rqzGkxXco2rDBOuVGMfk
      Cyc8QO5+Ym+0PPJOTWA6x9cTdCwSg2XfZoy7pRhiENTC7I78KZMa/NT+3Jpnksve
      pBA23tg7gTCi9f1tS+QjMJfz6pavK+0XcHS+4FEqg4B5l4f5pT9FGp3miI5z5uzv
      0gpi2SA4Q15HQAHGmzLtLCbuaVmivXqswvwktYbJ15Fhw8hcDhIg6pJZa2vO93gG
      ZGq87OydiIkk0pZxdabkpGxpbkKiIwK2+zFWDu3x604pR4b+rAMgrpEseD6TjLgr
      -----END RSA PRIVATE KEY-----
    fluentd_configs:
      example_input:
        enabled: true
        config: |
          <source>
            @type example
          </source>
      listen_on_5140:
        enabled: true
        config: |
          <source>
            @type syslog
            port 5140
            bind 127.0.0.1
            tag syslog
            format /^(?<time>[^ ]*\s*[^ ]* [^ ]*) (?<ident>[a-zA-Z0-9_\/\.\-]*)(?:\[(?<pid>[0-9]+)\])?(?:[^\:]*\:)? *(?<message>.*)$/
            time_format %b %d %H:%M:%S
          </source>
          <match syslog.**>

            @type null
          </match>
```

# License

```
Copyright (c) 2016 Tomoyuki Sakurai <y@trombik.org>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```

# Author Information

Tomoyuki Sakurai <y@trombik.org>
