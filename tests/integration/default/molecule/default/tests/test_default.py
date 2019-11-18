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


def test_icmp_from_client(host):
    ansible_vars = get_ansible_vars(host)
    if ansible_vars['inventory_hostname'] == 'client1':
        cmd = host.run("ping server1 -c 1 -q")

        assert cmd.succeeded


def test_icmp_from_server(host):
    ansible_vars = get_ansible_vars(host)
    if ansible_vars['inventory_hostname'] == 'server1':
        cmd = host.run("ping client1 -c 1 -q")

        assert cmd.succeeded


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


def get_ansible_vars(host):
    return host.ansible.get_variables()


def read_remote_file(host, filename):
    f = host.file(filename)
    assert f.exists
    assert f.content is not None
    return f.content.decode('utf-8')


def is_docker(host):
    ansible_facts = host.ansible('setup')['ansible_facts']
    # host.ansible.get_variables() in docker does not contain
    # 'ansible_virtualization_type'.
    #
    # https://github.com/philpep/testinfra/issues/447
    if 'ansible_virtualization_type' in ansible_facts:
        if ansible_facts['ansible_virtualization_type'] == 'docker':
            return True
    return False


def read_digest(host, filename):
    uri = "ansible://client1?ansible_inventory=%s" \
            % os.environ['MOLECULE_INVENTORY_FILE']
    client1 = host.get_host(uri)
    return read_remote_file(client1, filename)


def test_service(host):
    ansible_vars = get_ansible_vars(host)
    s = host.service(get_service_name(host))

    assert s.is_running
    # XXX in docker, host.service() does not work
    if is_docker(host):
        assert s.is_enabled


def test_find_digest1_on_client(host):
    ansible_vars = get_ansible_vars(host)
    if ansible_vars['inventory_hostname'] == 'client1':
        f = host.file('/tmp/digest1')

        assert f.exists


def test_find_digest2_on_client(host):
    ansible_vars = get_ansible_vars(host)
    if ansible_vars['inventory_hostname'] == 'client1':
        f = host.file('/tmp/digest2')

        assert f.exists


def test_find_digest1_in_logs(host):
    ansible_vars = get_ansible_vars(host)
    if ansible_vars['inventory_hostname'] == 'server1':
        content = read_digest(host, '/tmp/digest1')
        cmd = host.run("grep -- '%s' /tmp/fluentd.log.*", content)

        assert content is not None
        assert cmd.succeeded


def test_find_digest2_in_logs(host):
    ansible_vars = get_ansible_vars(host)
    if ansible_vars['inventory_hostname'] == 'server1':
        content = read_digest(host, '/tmp/digest2')
        cmd = host.run("grep -- %s /tmp/fluentd.log.*", content)

        assert content is not None
        assert cmd.succeeded
