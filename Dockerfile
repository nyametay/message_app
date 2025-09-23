FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into /data
COPY . .

# Expose Flask default port
EXPOSE 5000

# Run the data
CMD ["flask", "run", "--host=0.0.0.0"]
