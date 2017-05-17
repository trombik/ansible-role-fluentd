require "spec_helper"
require "serverspec"

fluentd_package_name = "td-agent"
fluentd_service_name = "td-agent"
fluentd_conf_dir     = "/etc/td-agent"
fluentd_config_dir   = "/etc/td-agent/conf.d"
fluentd_config_path  = "/etc/td-agent/td-agent.conf"
fluentd_user_name    = "td-agent"
fluentd_user_group   = "td-agent"
fluentd_gem_bin      = "/usr/sbin/td-agent-gem"
fluentd_certs_dir    = "/etc/td-agent/certs"
fluentd_buffer_dir   = "/var/spool/fluentd"
fluentd_unix_pipe_dir = "/var/tmp/fluentd"
fluentd_log_dir      = "/var/log/fluentd"
default_user         = "root"
default_group        = "root"

case os[:family]
when "freebsd"
  fluentd_user_name    = "fluentd"
  fluentd_user_group   = "fluentd"
  fluentd_package_name = "rubygem-fluentd"
  fluentd_service_name = "fluentd"
  fluentd_config_path  = "/usr/local/etc/fluentd/fluent.conf"
  fluentd_conf_dir     = "/usr/local/etc/fluentd"
  fluentd_config_dir   = "/usr/local/etc/fluentd/conf.d"
  fluentd_gem_bin = "/usr/local/bin/fluent-gem"
  fluentd_certs_dir    = "/usr/local/etc/fluentd/certs"
  default_group        = "wheel"
end
fluentd_plugin_dir = "#{fluentd_conf_dir}/plugin"

describe package(fluentd_package_name) do
  it { should be_installed }
end

describe file(fluentd_config_dir) do
  it { should be_directory }
  it { should be_mode 755 }
end

describe file(fluentd_plugin_dir) do
  it { should exist }
  it { should be_directory }
  it { should be_owned_by default_user }
  it { should be_grouped_into default_group }
  it { should be_mode 755 }
end

describe file(fluentd_log_dir) do
  it { should be_directory }
  it { should be_mode 755 }
  it { should be_owned_by fluentd_user_name }
  it { should be_grouped_into fluentd_user_group }
end

case os[:family]
when "redhat"
  describe file("/etc/sysconfig/td-agent") do
    it { should be_file }
    it { should be_mode 644 }
    it { should be_owned_by default_user }
    it { should be_grouped_into default_group }
    its(:content) { should match(/^TD_AGENT_OPTIONS=""$/) }
  end
when "ubuntu"
  describe file("/etc/default/td-agent") do
    it { should be_file }
    it { should be_mode 644 }
    it { should be_owned_by default_user }
    it { should be_grouped_into default_group }
    its(:content) { should match(/^TD_AGENT_OPTIONS=""$/) }
  end
when "freebsd"
  describe file("/etc/rc.conf.d") do
    it { should be_directory }
    it { should be_mode 755 }
    it { should be_owned_by default_user }
    it { should be_grouped_into default_group }
  end

  describe file("/etc/rc.conf.d/fluentd") do
    it { should be_file }
    it { should be_mode 644 }
    it { should be_owned_by default_user }
    it { should be_grouped_into default_group }
    its(:content) { should match(%r{^fluentd_flags="-p /usr/local/etc/fluentd/plugin"$}) }
  end
end

describe file(fluentd_config_path) do
  it { should be_file }
  it { should be_mode 644 }
  it { should be_owned_by default_user }
  it { should be_grouped_into default_group }
  its(:content) { should match(/log_level error/) }
  its(:content) { should match(/suppress_config_dump/) }
  its(:content) { should match(/^@include\s+#{ Regexp.escape(fluentd_config_dir + "/*.conf") }$/) }
end

describe service(fluentd_service_name) do
  it { should be_running }
  it { should be_enabled }
end

describe command("#{fluentd_gem_bin} list") do
  its(:stdout) { should match(/fluent-plugin-redis/) }
  its(:stdout) { should match(/fluent-plugin-secure-forward/) }
end

describe file("#{fluentd_config_dir}/listen_on_5140.conf") do
  its(:content) { should match(/@type syslog/) }
  its(:content) { should match(/port 5140/) }
end

describe port(5140) do
  it { should be_listening }
end

describe file(fluentd_certs_dir) do
  it { should be_directory }
  it { should be_mode 755 }
end

describe file("#{fluentd_certs_dir}/ca_key.pem") do
  it { should be_file }
  its(:content) { should match Regexp.escape("Proc-Type: 4,ENCRYPTED") }
  it { should be_mode 440 }
  it { should be_owned_by fluentd_user_name }
  it { should be_grouped_into fluentd_user_group }
end

describe file("#{fluentd_certs_dir}/ca_cert.pem") do
  it { should be_file }
  its(:content) { should match(/MIIDIDCCAggCAQEwDQYJKoZIhvcNAQEFBQAwTTELMAkGA1UEBhMCVVMxCzAJBgNV/) }
  it { should be_mode 644 }
  it { should be_owned_by fluentd_user_name }
  it { should be_grouped_into fluentd_user_group }
end

describe file(fluentd_buffer_dir) do
  it { should be_directory }
  it { should be_owned_by fluentd_user_name }
  it { should be_grouped_into fluentd_user_group }
  it { should be_mode 755 }
end

describe file(fluentd_unix_pipe_dir) do
  it { should be_directory }
  it { should be_owned_by fluentd_user_name }
  it { should be_grouped_into fluentd_user_group }
  it { should be_mode 755 }
end

describe file("#{fluentd_unix_pipe_dir}/fluentd.sock") do
  it { should be_pipe }
  it { should be_owned_by fluentd_user_name }
  it { should be_grouped_into fluentd_user_group }
  it { should be_mode 660 }
end
