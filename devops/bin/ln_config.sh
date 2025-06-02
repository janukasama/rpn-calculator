#!/usr/bin/env bash

system_info=$(uname -a | awk '{print tolower($0)}')

echo $system_info
if [[ $system_info == *"darwin"* ]]; then
  # This is a Mac Os System
  config_path=/etc/CONFIG
else
  # This is linux
  config_path=/CONFIG
fi

sudo ln -s ${PWD}/devops/configs/config.${AYOMI_ENV}.yml $config_path
