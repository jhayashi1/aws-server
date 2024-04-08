FROM public.ecr.aws/amazoncorretto/amazoncorretto:17.0.10-al2023-headless

ENV SERVER_PATH=/opt/server

COPY server/ ${SERVER_PATH}
EXPOSE 25565

RUN chmod +x ${SERVER_PATH}/start.sh
ENTRYPOINT /bin/bash ${SERVER_PATH}/start.sh