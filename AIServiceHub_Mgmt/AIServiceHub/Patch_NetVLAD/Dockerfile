# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /Patch-NetVLAD

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependenciesq
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install faiss-gpu
RUN pip install matplotlib
RUN pip install -r requirements.txt
# RUN sudo apt-get updata
# RUN sudo apt-get install ffmpeg libsm6 libxext6  -y
RUN sudo apt-get install libgl1-mesa-glx
# RUN pip install opencv-python
# RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python

# copy the content of the local src directory to the working directory
COPY ./ .

# command to run on container start
CMD [ "python", "./all_in_one.py" ]