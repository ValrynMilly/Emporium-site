FROM python:3.11.0
WORKDIR /Emporium-site
COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install tensorflow
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run"]