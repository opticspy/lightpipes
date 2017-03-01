FROM dockcross/manylinux-x64:latest
MAINTAINER guyskk "guyskk@qq.com"

# install fftw3
# http://www.fftw.org/fftw3_doc/Installation-on-Unix.html
# http://www.fftw.org/fftw-3.3.6-pl1.tar.gz
ADD fftw-3.3.6-pl1.tar.gz /tmp/fftw3/
WORKDIR /tmp/fftw3/fftw-3.3.6-pl1
# TODO: optimize build params
# https://git.archlinux.org/svntogit/packages.git/tree/trunk/PKGBUILD?h=packages/fftw#n34
RUN ./configure --enable-shared && make > /dev/null && make install

# build wheel
RUN /opt/python/cp36-cp36m/bin/pip install invoke
VOLUME /io/
WORKDIR /io/tools/linux
ENV TARGET=linux-x64
CMD ["/opt/python/cp36-cp36m/bin/inv", "build_all"]
