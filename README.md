<pre>
  _______                   _               _____             
 |__   __|                 | |             |  __ \            
    | | ___ _ __ ___  _ __ | | ___  _   _  | |  | | _____   __
    | |/ _ \ '_ ` _ \| '_ \| |/ _ \| | | | | |  | |/ _ \ \ / /
    | |  __/ | | | | | |_) | | (_) | |_| | | |__| |  __/\ V / 
    |_|\___|_| |_| |_| .__/|_|\___/ \__, | |_____/ \___| \_/  
                     | |             __/ |                    
                     |_|            |___/                                       
</pre>
Steps for Docker (Linux/Mac only)

1. Install Docker CE
	- Go to https://store.docker.com/search?type=edition&offering=community and find your distribution
	- Follow the steps and install Docker CE

2. Install docker-compose
	- Go to https://docs.docker.com/compose/install/ and follow the instructions for your distribution/operating system

3. git clone the temployBack repo into a folder (doesn't really matter where)

4. With sudo permissions, run docker-compose build from within the folder

5. After it's done building, run docker-compose up -d from within the folder

6. Connect to temploy-back.localhost to view the API

If you are having trouble connecting add temploy.localhost to your hosts file, in linux you can do this by editing your /etc/hosts file and adding 127.0.0.1 (press tab) temploy.localhost, and another line with 127.0.0.1 (press tab) temploy-back.localhost

(Use postman or a similar tool to connect to the API and view results)
