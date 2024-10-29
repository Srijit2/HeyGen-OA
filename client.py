import requests
import time
import random

class TranslationClient:
    def __init__(self, base_url, max_retries=5, initial_delay=1, max_delay=10):
        self.base_url = base_url
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
    
    def get_status(self, job_id, priority):
        delay = self.initial_delay
        for attempt in range(self.max_retries):
            try:
                #hits endpoint and gets return value.
                #raises error if one exists
                response = requests.get(f"{self.base_url}/status/{job_id}")
                response.raise_for_status()
                result = response.json().get("result")
                
                #Return if result fails or succeeds
                if result == "completed" or result == "error":
                    return result

                #If result is pending wait the delay amount of time before trying again
                elif result == "pending":
                    print(f"[Attempt {attempt + 1}] Status: pending. Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                    # uses exponential backoff to determine next delay
                    # The higher the priority the smaller the delay increase
                    if priority == "high":
                        delay = min(self.max_delay, delay + 1) 
                    elif priority == "medium":
                        delay = min(self.max_delay, delay * (1.5 + random.uniform(0, 0.5))) 
                    else:
                        delay = min(self.max_delay, delay * (1.5 + random.uniform(0.5, 1))) 
            except requests.RequestException as e:
                #if error occurs wait for some time and retry with increased delay
                print(f"Request failed: {e}")
                time.sleep(delay)
                delay = min(self.max_delay, delay * (1.5 + random.uniform(0, 0.5)))
        return "error"

# How to use
if __name__ == '__main__':
    client = TranslationClient("http://127.0.0.1:5000")
    job_id = "test_job"
    print(f"Testing status for job_id: {job_id}")
    final_status = client.get_status(job_id,"medium")
    print(f"Test completed. Final Status: {final_status}")