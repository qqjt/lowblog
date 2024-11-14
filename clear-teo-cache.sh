#!/bin/bash
# https://forum.gitlab.com/t/ci-cd-pipeline-get-list-of-changed-files/26847/2
# shellcheck disable=SC2207
files=($(git diff-tree --no-commit-id --name-only -r $1))
# Loop through the list
for file in "${files[@]}"; do
    echo "$file"
done
npm run teo -- "${files[@]}"