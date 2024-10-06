from flask import Flask, request, redirect
import itertools

app = Flask(__name__)

# Define the addresses of the replica servers
REPLICA_SERVERS = [
    "http://localhost:5001",
    "http://localhost:5002"
]

# Create an iterator for round-robin selection
replica_iterator = itertools.cycle(REPLICA_SERVERS)

@app.route('/request_video/<filename>', methods=['GET'])
def request_video(filename):
    # Get the next server from the iterator
    selected_server = next(replica_iterator)

     # Log the selected server URL
    print(f"Redirecting to: {selected_server}/video/{filename}")
    
    return redirect(f"{selected_server}/video/{filename}")

if __name__ == '__main__':
    app.run(port=5000)  # Specify the port for the controller
