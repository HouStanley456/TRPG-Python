Ubuntu 18.04 

--Python game on linebot--

you can use:

    -VM 
    -GCP Google Cloud Platform
    -AWS       



On CMD:

step 1:
    
    sudo apt-get update ;
    sudo apt-get install -y python3-pip unzip ;
    sudo timedatectl set-timezone Asia/Taipei ;
    pip3 install flask line-bot-sdk uwsgi ;
    source .profile 

step 2:
    
    sudo apt-get update ;
    sudo apt-get install -y nginx ;
    sudo timedatectl set-timezone Asia/Taipei; 
    sudo snap install core ;
    sudo snap refresh core ;
    sudo snap install --classic certbot ;
    sudo ln -s /snap/bin/certbot /usr/bin/certbot

step 3:
    
    sudo ln -s /etc/nginx/sites-available/line.conf /etc/nginx/sites-enabled/line.conf
    sudo vim /etc/nginx/sites-available/line.conf

paste on line.conf
   
    '''
    server {
        server_name YOUR_SERVER_NAME;

        # for LINE Bot
        location / {
            include uwsgi_params;
            #uwsgi_pass unix:/home/your_account/your_project_name/your_project_name.sock;
            uwsgi_pass 127.0.0.1:3000;
            #proxy_pass https://your_url;
        }
        # for Web or LIFF
        #location /test {
        #   
        #root /home/your_account/your_project_name;
        #alias /home/your_account/your_project_name;
        #}
    }

    '''
    #YOUR_SERVER_NAME need to change
    #Godaddy https://tw.godaddy.com/

step 4:
    
    sudo nginx -s reload
    sudo certbot --nginx
    
step 5:
    
    sudo apt-get install git-all
    sudo git clone https://github.com/HouStanley456/TRPG-on-LineBOT.git
    
step 6:
    
    sudo vim main.py
    
        Change Your CHANNEL_ACCESS_TOKEN and CHANNEL_SECRET :
        line_bot_api = LineBotApi('你的 CHANNEL_ACCESS_TOKEN')
        handler = WebhookHandler('你的 CHANNEL_SECRET')
       
step 7: 
    
    uwsgi -w main:app -s :3000
    
    
----Enjoy the game----

