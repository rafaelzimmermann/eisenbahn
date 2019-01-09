#!/bin/bash

git clone https://github.com/rafaelzimmermann/eisenbahn.git /opt/eisenbahn

cp /opt/eisenbahn/config.json.example /opt/eisenbahn/config.json
cp /opt/eisenbahn/install/eisenbahn.service /etc/systemd/system/eisenbahn.service

systemctl enable eisenbahn.service
