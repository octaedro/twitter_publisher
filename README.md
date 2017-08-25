# twitter_publisher
Twitter multiaccount publisher - Python
This robot automatically publishes tweets to the selected accounts.

Preconditions:
1) Have Python 2.7 installed
2) Have a mysql database

For this the following steps must be followed:
0)  - Execute in terminal: pip -r requirements.txt
1)  - Add the data to the configuration file
    - It is the connection to the database and the name of the table that will have the accounts
2)  - Run the file: deploy.py (run in terminal: python debug.py)
    - This will create the configuration table that you must fill
3)  - Fill in the table that contains the credentials for the twitter accounts
4)  - After the table has the credentials of the twitter accounts that you want to put online, rerun the file: deploy.py
    - This will create the tables that will contain the tweets
5)  - Run the file: run.py (run in terminal: python run.py)
6)  - Set a crontab that runs the run.py file

Twitter account table information:
This table contains the fields:
-`consumerkey` - twitter api
-`consumersecret` - twitter api
-`accesstoken` - twitter api
-`accesstokensecret` - twitter api
-`cuenta` - not necessary
-`palabra_clave`- keyword to be used when searching for new tweets
-`url_fb` - not necesary
-`fb_app_id` - not necessary
-`fb_app_secret` - not necessary
-`fb_token` - not necessary
-`tabla` - name of the table that we have the tweets of the account
-`publicar_cada` - time between tweet and tweet
            
