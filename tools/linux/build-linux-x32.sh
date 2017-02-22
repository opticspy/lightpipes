#!/bin/bash
set -ex
PROJECT_DIR=`(cd ../.. && pwd)`
docker build -t lightpipes-linux-x32 -f $PROJECT_DIR/tools/linux/linux-x32.Dockerfile .
docker run -v $PROJECT_DIR:/io lightpipes-linux-x32
ls -lh $PROJECT_DIR/wheelhouse/
