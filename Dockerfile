FROM nvidia/cuda:12.5.1-base-ubuntu22.04

WORKDIR /Emporium-site

# Copy local files to the container
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    python3-pip \
    python3-dev \
    python3-venv \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    v4l-utils \
    sudo

RUN apt-get update; apt install -y libgl1

# Upgrade pip and install Python packages
RUN pip3 install --upgrade pip && \
    pip3 install gdown

RUN git clone https://github.com/xinntao/ESRGAN.git

# Create the Models directory (just in case) and download the model file
RUN gdown 131jQJ8eHMg_8LgWMop-gfMpmMU0oshVx -O /Emporium-site/ESRGAN/models/RRDB_ESRGAN_x4.pth


# Install project dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install TensorFlow and PyTorch
RUN pip3 install tensorflow
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
RUN pip3 install opencv-python

# Expose the port the application runs on
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host", "0.0.0.0"]
