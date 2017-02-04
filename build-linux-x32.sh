#!/bin/bash
set -ex
docker build -t lightpipes-linux-x32 -f tools/linux-x32.Dockerfile .
docker run -v `pwd`:/io lightpipes-linux-x32
ls -lh wheelhouse/
