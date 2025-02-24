# Use the official Python base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy only the app.py file into the container
COPY app.py .

# Install FastAPI and Uvicorn
RUN pip install fastapi uvicorn

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

