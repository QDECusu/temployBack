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

TROUBLESHOOTING

If you're havinng problems with the backend API, there are a few commands you can use to attempt to troubleshoot

1. If you're having issues the number one cause of issues is migrations problems. Run the following to attempt to resolve that

    <pre>
        $ sudo docker exec -itt temploy-backend bash
        $ python3 manage.py makemigrations
        $ python3 manage.py migrate
    </pre>

    If this does not fix your issue then press CTRL-D to exit out of the container

2. Checking logs. Probably the most important thing to try to figure out what is going wrong

    <pre>
        $ sudo docker logs -f temploy-backend
    </pre>

   This will show you the error logs for the docker container. It should provide you with enough information to see exactly what is going wrong

3. Rebuilding container. Do this if nothing else has helped you at all, but don't expect it to fix anything.

    <pre>
        $ cd to your temploy backend directory
        $ sudo docker-compose down
        $ sudo docker-compose build
        $ sudo docker-compose up -d
    </pre>
