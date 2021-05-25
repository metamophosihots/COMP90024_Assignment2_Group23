# Deploy front-end solution on instances

## Copy all files to the instance
Navigate to front-end-deploy-file directory.\
`cd ~/front-end-deploy-file/`  
Copy all directories to instance.\
`scp -i <key> -r * <username>@<ip_address>:~/front_end/`  

## Deploy web-app on the instance
Log into the instance.\
`ssh -i <key> <username>@<ip_address>`  
### Install Node.js
Install the latest version of Node.js and npm.\
`sudo apt-get update`

`curl -sL https://deb.nodesource.com/setup_112.x | sudo -E bash -`  

`sudo apt install nodejs -y`

### Install project dependencies on the instance
Naviagate to where you put these files and get into dashboard, in this example is front_end.\
`cd ~/front_end/dashboard`  
Install all of dependencies  
`npm install`  
Navigate to server directory, install `express` package to be able to use Node.js to run the web-app.\
`cd ~/front_end/server`  
`npm install express`  

### Install PM2 to run the site
To keep the site running at all times, PM2 process manager can be used for Node.js.\
`sudo npm install -g pm2`\
Navigate to the server directory and run the site with PM2.
`cd ~/front_end/server`\
`pm2 start server.js`\

## After deployment
Now the site is running on `http://<ip_address>:3000`, 
to be able to see the visulization of data, the Couchdb needs to be deployed and data and views should be prepared. 
All of these will be showed in other part of this repository.
Look\ 
[https://github.com/metamophosihots/COMP90024_Assignment2_Group23/blob/main/README.md]
(https://github.com/metamophosihots/COMP90024_Assignment2_Group23/blob/main/README.md)\ 
for how to use website and play around with dashboard.
