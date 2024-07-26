FROM nvidia/cuda:12.5.1-base-ubuntu22.04

WORKDIR /Emporium-site
COPY . .

RUN apt-get update
RUN apt-get install -y git 
RUN apt install -y python3-pip 
RUN apt install -y python3-dev 
RUN apt install -y python3-venv 
RUN apt install -y libglib2.0-0
        

RUN git clone https://github.com/xinntao/ESRGAN.git

ADD ESRGAN /Emporium-site


RUN pip3 install --upgrade pip
RUN pip3 install gdown
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install tensorflow
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
RUN gdown 131jQJ8eHMg_8LgWMop-gfMpmMU0oshVx -O ESRGAN/Models/RRDB_ESRGAN_x4.pth

EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0"]