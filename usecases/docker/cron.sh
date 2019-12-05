#!/bin/bash

set -e
scriptname=$(basename $0)
lock="/var/lock/${scriptname}"

(
  # Wait for lock on /var/lock/.myscript.exclusivelock (fd 200) for 10 seconds
  flock -x -w 10 200 || exit 1
  curl -X POST -H 'Content-type: application/json' --data '{"text":"Starting pipeline update!"}' https://hooks.slack.com/services/12345/9876/abc123

  curl -X POST -H 'Content-type: application/json' --data '{"text":"Pulling latest docker!"}' https://hooks.slack.com/services/12345/9876/abc123
  timeout 10m gcloud docker -- pull us.gcr.io/someproject/test_container:latest

  curl -X POST -H 'Content-type: application/json' --data '{"text":"Running pipeline phase 1!"}' https://hooks.slack.com/services/12345/9876/abc123
  timeout 2h docker run --name pipeline_runner --cpus 2 --memory 16GB --env-file=/home/user/pipeline.env --rm --entrypoint "invoke" us.gcr.io/someproject/test_container pipeline_part_one

  curl -X POST -H 'Content-type: application/json' --data '{"text":"Running pipeline phase 1!"}' https://hooks.slack.com/services/12345/9876/abc123
  timeout 1h docker run --name pipeline_runner --cpus 2 --memory 12GB --env-file=/home/user/pipeline.env --rm --entrypoint "invoke" us.gcr.io/someproject/test_container pipeline_part_two

  curl -X POST -H 'Content-type: application/json' --data '{"text":"Finished pipeline update!"}' https://hooks.slack.com/services/12345/9876/abc123
) 200>$lock
