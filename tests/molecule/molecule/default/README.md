## scenario `default`

### Description

The scenario creates two instances, a `fluentd` server, and a client.

The client has a `syslog` setting to forward all logs to remote `syslog`
server.

A `fluentd` listener on the server listens on UDP port 5140 and logs `syslog`
entries on local file.

The scenario has a side-effect play that sends two log entries via `logger(1)`
and Unix socket.

The test will see if these log entries are actually logged in the log file.
