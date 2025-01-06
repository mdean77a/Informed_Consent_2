# Trying to put qdrant into same container as chainlit application

FROM qdrant/qdrant:latest 
RUN apt-get update && apt-get install -y \
    --no-install-recommends curl ca-certificates\
    && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
# ENV PATH="/root/.local/bin/:$PATH"

# # Set te home directory and path
ENV HOME=/home/user \
    PATH="/home/user/.local/bin:/root/.local/bin/:$PATH"
           

# # NEEDED FOR CHAINLIT IN HUGGING FACE SPACES
ENV UVICORN_WS_PROTOCOL=websockets

# # Set the working directory
WORKDIR $HOME/app

# # Copy the app to the container
COPY --chown=user . $HOME/app
RUN chmod +x entrypoint.sh
# # Install the dependencies
RUN uv sync --frozen

# # Expose the ports
EXPOSE 7860 6333
ENTRYPOINT ["./entrypoint.sh"]

