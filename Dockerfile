# Start with qdrant image
FROM qdrant/qdrant:latest 

# Need curl and ca-certificates
RUN apt-get update && apt-get install -y \
    --no-install-recommends curl ca-certificates\
    && rm -rf /var/lib/apt/lists/*

# RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/custom/path" sh
# Install uv - it installs in /root/.local/bin
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh


# Set the home directory and path, need access to uv
ENV HOME=/home/user \
    PATH="/home/user/.local/bin:/root/.local/bin/:$PATH"

# # NEEDED FOR CHAINLIT IN HUGGING FACE SPACES
ENV UVICORN_WS_PROTOCOL=websockets

ENV QDRANT_ENABLE_DASHBOARD=true
# Set the working directory
WORKDIR $HOME/app

RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=$HOME/app sh
# # Copy the app to the container
COPY --chown=user . $HOME/app

RUN chmod 777 entrypoint.sh

# # Install the dependencies
RUN uv sync --frozen

# # Expose the ports
EXPOSE 7860 6333
ENTRYPOINT ["./entrypoint.sh"]
