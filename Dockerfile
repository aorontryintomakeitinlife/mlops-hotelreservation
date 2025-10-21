##before this we did our github integration using special key , credentials,a named jenkins pipeline, 
##IMPORTED IMAGE
FROM python:slim

##we dont want out environment to oveWrrite our .pyc files fot hat

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 
##all working directory will be under this, CREATED APP DIRECTOTY
WORKDIR /app
##below WE INSTALLED are lightgbm model dependiceis
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libgomp1 \
    cargo \
    git \
    cmake \
    wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

##CODE ALL CODE FROM PROJECT DIRECTORY
COPY . .

# Upgrade pip, setuptools, wheel to avoid build warnings
RUN pip install --upgrade pip setuptools wheel

# Install heavy dependencies with binary wheels
RUN pip install numpy pandas lightgbm pyarrow --prefer-binary
##no cache dir to avoid taking the pycACHE FILES
##BELOW NOW WE INSTALL ALL PACKAGES USING OUR SETUP.PY 
RUN pip install --no-cache-dir -e .

##trainnojg our WHOLE model
RUN python pipeline/training_pipeline.py
## SERT UP PORT -FLASK APP WILL RUN
EXPOSE 5000
#BELOW COMMAND TO RUN APP
CMD ["python", "application.py"]




##THIS IS COMPLETION OF OUR 3RD STEP DOCKERISATION OF PROJECT(DOCKERFILE)
##next we move to create a venv in your jenkins



