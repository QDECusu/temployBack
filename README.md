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
Steps for Cloud9

run the following commands from the command line.

1. sudo pip3 install --upgrade pip

2. sudo pip3 install --upgrade django

Follow this by changing your python settings in cloud9

3. Run -> Run Configurations -> Manage -> Python Support -> Python Version -> Python 3

Then you'll need to create a custom runner because Cloud9 hasn't setup anything allowing you to do this automatically which stinks

4. mkdir ~/workspace/.c9/runners && cp ~/workspace/cloud9/CustomDjango.run ~/workspace/.c9/runners

Finally you'll set this as your primary runner

5. Click Run Project which should try to run django and fail

6. In the "Django - Stopped" tab at the bottom of the editor click on Runner: Django on the right hand side and select "CustomDjango"

7. You'll need to modify your ~/TemployProj/setting.py file and change the allowed hosts to include your cloud9 url.

Should be good to go at this point.
