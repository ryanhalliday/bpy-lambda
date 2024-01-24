FROM python:3.10

RUN python -m pip install awslambdaric

# Blender requirements
RUN apt-get update && apt-get install -y \
    wget \
    # to extract tar.xz
	xz-utils \
    # from https://github.com/blender/blender/blob/v3.3.0/release/freedesktop/snap/blender-snapcraft-template.yaml
    libxcb1 \
    libxext6 \
    libx11-6 \
    libxi6 \
    libxfixes3 \
    libxrender1 \
    libxxf86vm1 \
    # libGL
    libgl1-mesa-glx \
    # libxkbcommon.so.0 needed since 3.4.0 apparently
    libxkbcommon0 \
    # libSM.so.6 needed since 3.5.1 apparently
    libsm6

RUN python -m pip install bpy==3.6.0

ARG FUNCTION_DIR="/home/app/"
RUN mkdir -p ${FUNCTION_DIR}
WORKDIR ${FUNCTION_DIR}

COPY requirements.txt ${FUNCTION_DIR}
RUN python -m pip install -r requirements.txt

COPY app.py ${FUNCTION_DIR}

CMD python -m awslambdaric "app.lambda_handler"
