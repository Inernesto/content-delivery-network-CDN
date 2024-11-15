# content-delivery-network-CDN
This is a content-delivery-network (CDN) utilizing HTTP/2 throughout the data communication accross all the entities (client and server). This was done using the Python programing language (for core data transfers), PHP for web application with APACHE.

## Setup Instructions

1. **Download and Install Python**

   - Go to the [official Python website](https://www.python.org/downloads/).
   - Download the latest version of Python for your operating system.
   - Follow the installation instructions specific to your OS.

   > Make sure to check the box to **Add Python to PATH** during the installation process.

2. **Create a Virtual Environment**

   Once Python is installed, open a terminal or command prompt and run the following commands:

   ### For Windows:
   ```bash
   python -m venv myenv
   ```
   
   ### For Mac/Linux:
   ```bash
   python3 -m venv myenv
   ```

3. **Activate a Virtual Environment**
	
	Activate the virtual environment and install the following library:
	
	### For Windows:
	```bash
	myenv\Scripts\activate
    pip install grpcio
	pip install watchdog
	```
	
	### For Mac/Linux:
	```bash
	source myenv/bin/activate
	pip install grpcio
	pip install watchdog
	```
	
4. **Download and Install PHP**
   - Go to the [official PHP website](https://www.php.net/downloads/).
   - Download the latest version of PHP for your operating system.
   - Follow the installation instructions specific to your OS.
   - On Windows, you may need to configure the PHP executable in the System Environment Variables to make it accessible globally.
   
5. **Download and Install Apache**
	- Go to the [official Apache HTTP server](https://httpd.apache.org/downloads.cgi).
	- Download the version of Apache server that is compartible with the version of PHP you downloaded in 4. To know the version of Apache to download, check the php folder, you should see an application extension file like this "php8apache2_4.dll", this suggests that Apacche 2.4 is needed for this PHP version 8.
	- On Windows, you may need to configure the Apacche executable in the System Environment Variables to make it accessible globally.


## To run the code locally

1. **Start the various python servers**
	- Open a terminal with administrative privileges (to enable the program to create files an folders accordingly).
	- Navigate to the python script directory and start the python script. This should be done for all the replica servers and also the origin server preferably on separate terminals.
	
	### To run the replica servers
	```bash
	python replica_grpc_server.py
	```
	
	### To run the origin server
	```bash
	python origin_grpc_server.py
	```
	
2. **Update Your Local Hosts File**
	- To point the domain names (main-cdn.local, origin.local, replica-1.local, replica-2.local, replica-3.local) to your local machine, you'll need to edit your hosts file.
	
	### For Windows
	- Open C:\Windows\System32\drivers\etc\hosts with Notepad (run as Administrator).
	- Add the following lines:
	> 127.0.0.1   origin.local
	> 127.0.0.1   main-cdn.local
	> 127.0.0.1   replica-1.local
	> 127.0.0.1   replica-2.local
	> 127.0.0.1   replica-3.local
	
	### For Linux/Mac
	```bash
	sudo nano /etc/hosts
	```
	- Add the following lines **(NB: Remember to enable the Virtual Hosts configuration file. You can look this up online.)**:
	> 127.0.0.1   origin.local
	> 127.0.0.1   main-cdn.local
	> 127.0.0.1   replica-1.local
	> 127.0.0.1   replica-2.local
	> 127.0.0.1   replica-3.local
	
3. **Start the Apache server**
	- In the downloaded or cloned repo from github, you will see a httpd conf file "httpd.conf", replace this with the httpd.conf file in "Apache/conf" directory of the version you installed.
	- Start the Apache service.
	
	### To start the Apacche service
	```bash
	httpd.exe -k Start
	```
	
	### To stop the Apacche service
	```bash
	httpd.exe -k stop
	```
	
4. **Start your browser from the command line and ignore the certificate errors**
	- This makes it possible to run the program on the browser locally without the browser having to always validate the SSL/TLS certificate (since they are self-signed and not from a recognized organization). Ignore this step if you are able to use SSL/TLS certificates from trusted and recognized organizations.
	
	> Use this only for testing purposes on trusted networks, as it can expose you to security risks.
	
	- Open a terminal and run the following code:
	
	### For Windows
	```bash
	start chrome --ignore-certificate-errors
	```
	
	### For macOS
	```bash
	open -na "Google Chrome" --args --ignore-certificate-errors
	```
	
	### For Linux
	```bash
	google-chrome --ignore-certificate-errors
	```

5. **Run the application in the browser**
	- In the browser tab that was launched in step 4. run the cdn application.
	
	### To upload contents
	https://origin.Local
	
	### To watch the videos from the replica servers
	https://main-cdn.local
	
	



	

