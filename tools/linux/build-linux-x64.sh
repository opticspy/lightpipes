#!/bin/bash
set -ex
PROJECT_DIR=`(cd ../.. && pwd)`
docker build -t lightpipes-linux-x64 -f $PROJECT_DIR/tools/linux/linux-x64.Dockerfile .
docker run -v $PROJECT_DIR:/io lightpipes-linux-x64
ls -lh $PROJECT_DIR/wheelhouse/
