FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the documentation files
COPY docs ./docs
COPY mkdocs.yml .

# Expose the port for the MkDocs server
EXPOSE 8000

# Command to run the MkDocs server
CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:12000"]