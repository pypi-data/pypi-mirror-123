#!/bin/bash

# debug mode
set -x

# fail script at first failed command
set -e

echo "Building $CI_PROJECT_NAME..."

echo "{
  \"name\": \"$CI_PROJECT_NAME\",
  \"CONSUMPTION_ECR_REG\": \"$CONSUMPTION_ECR_REG\",
  \"commit\": \"$CI_COMMIT_SHORT_SHA\",
  \"CI_PROJECT_NAME\": \"$CI_PROJECT_NAME\",
  \"CI_PIPELINE_ID\": \"$CI_PIPELINE_ID\"
}"

# Build an image setup for testing
# Also inject the env vars used by the healthcheck endpoint.
docker build \
 -f Dockerfile.test \
 -t "test-$CI_COMMIT_SHORT_SHA" \
 --build-arg PYTHON_COMMONS_API_KEY="${PYTHON_COMMONS_API_KEY}" \
 --build-arg IMAGE="base-$CI_COMMIT_SHORT_SHA" \
 .

pwd
ls
cd lib/
pwd

# Run the tests.
# Adding pytest -vv enables very verbose logging so tests take twice as long.
docker run  -P "test-$CI_COMMIT_SHORT_SHA" /bin/bash -c 'cd lib/tests/; pytest -vv -s'
