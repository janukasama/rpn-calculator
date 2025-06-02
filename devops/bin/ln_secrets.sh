#!/usr/bin/env bash

system_info=$(uname -a | awk '{print tolower($0)}')

if [[ $system_info == *"darwin"* ]]; then
  # This is a Mac Os System
  secrets_folder=/etc/secrets/rpn-calculator
else
  # This is linux
  secrets_folder=/run/secrets/rpn-calculator
fi

read -p "Are you sure you are on a dev environment? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    if [[ -d "${secrets_folder}" ]]
    then
        sudo rm -rf ${secrets_folder}
    fi
    sudo mkdir -p ${secrets_folder}

    for filename in ./devops/secrets/*; do
      secret_name=`basename ${filename}`
      sudo ln -s ${PWD}/${filename} ${secrets_folder}/${secret_name}
    done
fi

