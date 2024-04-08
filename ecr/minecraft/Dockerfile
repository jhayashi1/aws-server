FROM public.ecr.aws/amazoncorretto/amazoncorretto:17.0.10-al2023-headless
COPY server/ /opt/server/

EXPOSE 25565
RUN ["chmod", "+x", "/opt/server/start.sh"]

# ENTRYPOINT [ "/bin/bash", "/opt/server/start.sh" ]