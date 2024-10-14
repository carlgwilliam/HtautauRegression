#!/bin/bash

# Find the base directory of the repository
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Setup the common conda environment
ENV_PATH="conda"
[ -d "${ENV_PATH}" ] && source "${ENV_PATH}"/bin/activate

export PYTHONPATH=${BASE_DIR}/python/:$PYTHONPATH
