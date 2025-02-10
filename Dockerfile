# Use an official Python runtime
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Copy the secrets file into the Streamlit configuration folder
RUN mkdir -p ~/.streamlit
COPY /secrets.toml /root/.streamlit/secrets.toml

# Expose the default Streamlit port
EXPOSE 8501

# Command to run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

