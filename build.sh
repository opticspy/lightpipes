#!/bin/bash

docker build -t lightpipes-linux-x64 -f tools/linux-x64.Dockerfile . \
&& docker run --rm -ti -v `pwd`:/io lightpipes-linux-x64 \
&& ls wheelhouse/
