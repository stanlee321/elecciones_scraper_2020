FROM python:3.8-alpine3.10

ENV PROJ_DIR="/code"
ENV LOG_FILE="${PROJ_DIR}/app.log"
ENV CRON_SPEC="* * * * *" 
WORKDIR ${PROJ_DIR}

RUN apk update
RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories
RUN apk update

RUN apk --no-cache --update-cache add gcc gfortran build-base wget freetype-dev libpng-dev openblas-dev 
RUN apk --update add libgcc musl-dev jpeg-dev zlib-dev
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

# Chrome
RUN apk add chromium chromium-chromedriver

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
CMD crond  && tail -f ${LOG_FILE} #crond runs per default in the background