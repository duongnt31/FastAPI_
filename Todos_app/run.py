import subprocess

# Define commands to run
uvicorn_command = ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
streamlit_command = ["python3", "-m", "streamlit", "run", "src/stream.py", "--server.port", "8501", "--server.address", "0.0.0.0"]

# Run commands concurrently
uvicorn_process = subprocess.Popen(uvicorn_command)
streamlit_process = subprocess.Popen(streamlit_command)

# Wait for both processes to finish
uvicorn_process.wait()
streamlit_process.wait()
