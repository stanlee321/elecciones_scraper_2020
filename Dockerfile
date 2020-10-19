FROM python:3.7-alpine3.8

ENV PROJ_DIR="/code"
ENV LOG_FILE="${PROJ_DIR}/app.log"
ENV CRON_SPEC="*/2 * * * *"

ENV PATH="/usr/bin/chromedriver:${PATH}" 

WORKDIR ${PROJ_DIR}

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.8/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.8/community" >> /etc/apk/repositories

RUN apk update && apk add --no-cache bash \
        alsa-lib \
        at-spi2-atk \
        atk \
        cairo \
        cups-libs \
        dbus-libs \
        eudev-libs \
        expat \
        flac \
        gdk-pixbuf \
        glib \
        libgcc \
        libjpeg-turbo \
        libpng \
        libwebp \
        libx11 \
        libxcomposite \
        libxdamage \
        libxext \
        libxfixes \
        tzdata \
        libexif \
        udev \
        xvfb \
        zlib-dev \
        chromium \
        chromium-chromedriver
# install chromedriver

# upgrade pip
RUN pip install --upgrade pip

RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt "${PROJ_DIR}/requirements.txt"
#RUN pip install --no-cache-dir  -r requirements.txt
RUN pip install -r requirements.txt
COPY . ${PROJ_DIR}

RUN echo "${CRON_SPEC} python ${PROJ_DIR}/main.py >> ${LOG_FILE} 2>&1" > ${PROJ_DIR}/crontab
RUN touch ${LOG_FILE} # Needed for the tail
RUN crontab ${PROJ_DIR}/crontab
RUN crontab -l
CMD crond  && tail -f ${LOG_FILE}