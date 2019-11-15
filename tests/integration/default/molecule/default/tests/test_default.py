import os

import testinfra
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


def read_remote_file(host, filename):
    f = host.file(filename)
    assert f.exists
    assert f.content is not None
    return f.content.decode('utf-8')


def read_digest(host, filename):
    uri = "ansible://client1?ansible_inventory=%s" \
            % os.environ['MOLECULE_INVENTORY_FILE']
    client1 = host.get_host(uri)
    return read_remote_file(client1, filename)


def test_service(host):
    s = host.service(get_service_name(host))

    assert s.is_running
    assert s.is_enabled


def test_digests(host):
    ansible_vars = host.ansible.get_variables()
    if ansible_vars['inventory_hostname'] == 'server1':
        content1 = read_digest(host, '/tmp/digest1')
        content2 = read_digest(host, '/tmp/digest2')
        cmd1 = host.run("grep -- %s /tmp/fluentd.log.*", content1)
        cmd2 = host.run("grep -- %s /tmp/fluentd.log.*", content2)

        assert content1 is not None
        assert cmd1.succeeded
        assert content2 is not None
        assert cmd2.succeeded
    elif ansible_vars['inventory_hostname'] == 'client1':
        f = host.file('/tmp/digest1')

        assert f.exists
