# Use the full Python 3.11 image as the base, since it worked reliably
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
# --no-cache-dir makes the image slightly smaller
# --trusted-host pypi.python.org -trusted-host pypi.org -trusted-host files.pythonhosted.org might be needed if network issues occur
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code and the model into the working directory
# Ensure predict_app.py and the .joblib file are in the same directory as the Dockerfile
COPY predict_app.py .
COPY titanic_logistic_regression_model.joblib .

# Expose the port the Flask app runs on
EXPOSE 5000

# Define the command to run the application when the container starts
# Use gunicorn or waitress for production later, but Flask dev server is fine for now.
# Use ["python", "predict_app.py"] instead of just "python predict_app.py" for better signal handling
CMD ["python", "predict_app.py"]