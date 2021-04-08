#!/bin/sh
set -e

systemctl daemon-reload
systemctl enable robotic-arm
systemctl start robotic-arm
