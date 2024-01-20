#!/bin/bash

set -o errexit
set -o nounset

# exec watchfiles celery.__main__.main --args '-A config.celery worker -l INFO'

exec celery -A config.celery worker -l DEBUG --pool=solo -E
exec celery -A config.celery beat -S django