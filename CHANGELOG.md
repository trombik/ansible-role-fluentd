## Release 2.0.1

* dd8155f bugfix: bundle lock x86_64-linux for CI
* db53fbc doc: update the example
* ee5c56a bugfix: fix tests for CentOS
* 64ddc91 ci: add GitHub workflows
* bbe14d9 bugfix: update box versions, ruby versions, and repo URLs
* 7f5f171 bugfix: update gems
* 2f20c2f bugfix: wrong path to fluent-cat
* e6f9056 bugfix: add RedHat to os_project_fluent_cat
* 8285a21 bugfix: add treasuredata repository
* 78efc7f bugfix: install rsyslog if not installed
* 380bab4 QA
* 56d075e bugfix: add travisci_centos7
* 99c7d69 doc: update README.md
* 2a159a3 bugfix: update molecule.yml and add docker role to travisci_ubuntu1804
* bfb2dc5 bugfix: QA
* bc829a9 bugfix: QA
* fc09084 bugfix: QA
* 61bde6f feature: enable molecule in travis
* 8f11fde feature: introduce molecule tests
* 7698e2a QA
* d4d60c2 bugfix: update gitignore

## Release 2.0.0

* da32a5b bugfix: update README
* a6def1a backward incompatible, bugfix: change the meaning of fluentd_flags

## Release 1.7.0

* 9c6d86c feature: introduce fluentd_extra_packages

## Release 1.6.0

* d5e2cd3 feature: introduce fluentd_extra_files
* 7930aad bugfix: add required gem for integration test
* 4dd9607 bugfix: update box version

## Release 1.5.1

* 20bf866 bugfix: QA
* 19bb60b bugfix: QA
* 2b18620 bugfix: remove stale patch and tasks
* 5a7f2c4 bugfix: refactor the role
* 94e73f4 bugfix: QA
* cb7a13e bugfix: remove hard-dependency
* f800d67 bugfix: restore ansible_verbosity value
* 4e1c588 update the example plugin
* 994ff5c bugfix: QA
* 7d50b37 [bugfix] QA (#8)
* 16632a0 [bugfix] drop invalid tag from meta (#7)

## Release 1.5.0

* 707f446 [feature][bugfix] Support OpenBSD 6.3, drop EoLed release (#5)

## Release 1.4.2

* 0429259 [bugfix] QA and follow the latest fluentd plug-in API in the example plug-in (#3)

## Release 1.4.1

* 6e879c8 [bugfix] update rubocop to the latest (#1)
* d1f941b [bugfix] remove the registered variable and `when` (#54)

## Release 1.4.0

* bdebcdf [bugfix][feature] introduce fluentd_plugins_to_create (#50)
* ef6b8c8 [feature] introduce fluentd_extra_groups (#48)

## Release 1.3.0

* 35c0b41 [feature][bugfix] support reloading fluentd (#45)
* e877178 remove hard-coded ruby installation tasks (#43)
* 576e7d0 [feature] support OpenBSD (#41)
* 522a0fd [feature] support fluentd_pid_dir and fluentd_pid_file (#39)

## Release 1.2.0

* b6b3e2d [enhancement] explain fluentd_plugin_dir and fluentd_flags (#36)
* ebd748a [feature] introduce fluentd_flags and fluentd_plugin_dir (#35)

## Release 1.1.1

* c5ba769 [bugfix] patch record_transformer plug-in (#32)
* f8bebb9 [bugfix] work around SNI issue (#29)

## Release 1.1.0

* f4416ee [bugfix] do not hard-code system-wide configuration (#27)
* 205258d [feature] support ubuntu 16.04 (#26)
* 4425f7a bugfix: do not hard-code release name (#25)
* a37cf5f [feature] create fluentd_log_dir if defined (#24)
* b6bff62 [bugfix] fix conditionals to test emptiness (again) (#23)

## Release 1.0.1

* 3e7b53a [bugfix] fix conditionals to test emptiness (#18)

## Release 1.0.0

* Initial release
