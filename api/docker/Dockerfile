# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Install the required packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the local code to the container
COPY ./main.py /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
