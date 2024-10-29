# Client instructions

1. To run the client start up the server by running:
   
   python server.py 

2. Run the client

   python client.py


# Customization

Depending on client needs it can set a job to different priorities ("high", "medium", "low"). 
The higher a priority the lower the delay between endpoint hits. 

This can be selected on line 50 of client.py

final_status = client.get_status(job_id,"medium")

In the example above the priority is set to medium. 
