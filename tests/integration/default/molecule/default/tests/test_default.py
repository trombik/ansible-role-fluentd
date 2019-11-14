import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root' or f.group == 'wheel'


def get_service_name(host):
    if host.system_info.distribution == 'freebsd':
        return 'fluentd'
    if host.system_info.distribution == 'openbsd':
        return 'fluentd'
    elif host.system_info.distribution == 'ubuntu':
        return 'td-agent'
    elif host.system_info.distribution == 'centos':
        return 'td-agent'
    raise NameError('Unknown distribution')


def test_service(host):
    s = host.service(get_service_name(host))

    assert s.is_running
    assert s.is_enabled
