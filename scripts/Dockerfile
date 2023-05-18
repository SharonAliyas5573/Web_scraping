# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster



# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .


# Install any needed packages specified in requirements.txt
RUN pip install  -r requirements.txt

# Copy the rest of the script folder contents into the container
COPY . .

# Define the command to run when the container starts
CMD ["python", "start.py"]
