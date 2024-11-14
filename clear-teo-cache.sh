#!/bin/bash
# https://forum.gitlab.com/t/ci-cd-pipeline-get-list-of-changed-files/26847/2
# shellcheck disable=SC2207
files=($(git diff-tree --no-commit-id --name-only -r $CI_COMMIT_SHA))
# Loop through the list
for file in "${files[@]}"; do
    echo "$file"
done

echo "$BASE_URL"
echo "$TENCENTCLOUD_SECRET_ID"
echo "$TENCENTCLOUD_SECRET_KEY"
echo "$TENCENTCLOUD_TEO_ZONE_ID"

export BASE_URL=$BASE_URL
export TENCENTCLOUD_SECRET_ID=$TENCENTCLOUD_SECRET_ID
export TENCENTCLOUD_SECRET_KEY=$TENCENTCLOUD_SECRET_KEY
export TENCENTCLOUD_TEO_ZONE_ID=$TENCENTCLOUD_TEO_ZONE_ID
npm run teo -- "${files[@]}"