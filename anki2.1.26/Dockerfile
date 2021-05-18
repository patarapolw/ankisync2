FROM x11docker/lxqt
RUN apt-get update
RUN apt-get install -y wget build-essential bzip2 xdg-utils
RUN wget -q https://github.com/ankitects/anki/releases/download/2.1.26/anki-2.1.26-linux-amd64.tar.bz2
RUN tar -xf anki-2.1.26-linux-amd64.tar.bz2
RUN cd anki-2.1.26-linux-amd64 && make && make install

RUN apt-get install -y locales libnss3 mpv
RUN sed -i '/en_US.UTF-8/s/^#//g' /etc/locale.gen
RUN locale-gen
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
