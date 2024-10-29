from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

jobs = {}

@app.route('/status/<job_id>', methods=['GET'])
def get_status(job_id):
    #gets job
    #If the job_id does not exist create a new one with random delay from 5 to 15 seconds
    job = jobs.get(job_id, {"start_time": time.time(), "delay": random.uniform(5, 15)})
    elapsed = time.time() - job["start_time"]
    
    #Return error if job fails
    if job.get("status") == "error":
        return jsonify({"result": "error"})
    
    #Return pending if time left to finish job
    if elapsed < job["delay"]:
        jobs[job_id] = job 
        return jsonify({"result": "pending"})
    
    #return completed if job succeeds
    job["status"] = "completed"
    jobs[job_id] = job
    return jsonify({"result": job["status"]})

# Starts server
if __name__ == '__main__':
    app.run(debug=True)
