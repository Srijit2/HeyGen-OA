import threading
from time import sleep
from client import TranslationClient

def run_server():
    from server import app
    app.run()

def test_client():
    client = TranslationClient("http://127.0.0.1:5000")
    job_id = "test_job"
    print(f"Testing status for job_id: {job_id}")
    final_status = client.get_status(job_id,"medium")
    print(f"Test completed. Final Status: {final_status}")

if __name__ == "__main__":
    # Start server
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    sleep(1)  # Give server time to start

    # Run the client test
    test_client()
    server_thread.join()
