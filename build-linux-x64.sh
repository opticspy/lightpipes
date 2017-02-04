#!/bin/bash
set -ex
docker build -t lightpipes-linux-x64 -f tools/linux-x64.Dockerfile .
docker run --rm -v `pwd`:/io lightpipes-linux-x64
ls -lh wheelhouse/
