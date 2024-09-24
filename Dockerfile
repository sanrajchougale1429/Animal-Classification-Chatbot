# Use the official Python 3.11 image from Docker Hub
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port Streamlit runs on (default is 8501)
EXPOSE 8501

# Define the command to run the Streamlit app
CMD ["streamlit", "run", "qachat.py"]
