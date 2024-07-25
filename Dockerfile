FROM python:3.11.0
WORKDIR /Emporium-site
COPY . .
RUN pip3 install --upgrade pip
RUN apt update; apt install -y libgl1
RUN git clone https://github.com/xinntao/ESRGAN.git
RUN pip3 install gdown
RUN python3 -c "gdown 131jQJ8eHMg_8LgWMop-gfMpmMU0oshVx -O ESRGAN/Models/RRDB_ESRGAN_x4.pth"
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install tensorflow
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0"]