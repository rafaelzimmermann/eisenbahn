#!/bin/bash

git clone https://github.com/rafaelzimmermann/eisenbahn.git /opt/eisenbahn

cp /opt/eisenbahn/install/eisenbahn.service /etc/systemd/system/eisenbahn.service

systemctl enable eisenbahn.service
