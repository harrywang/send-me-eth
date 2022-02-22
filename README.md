# About
a simple automated tool to get testing ether from https://www.rinkebyfaucet.com/

The main goal is to show the followings:

- Automate browsers using Selenium
- Send emails using SendGrid
- Schedule scripts using `crontab`
- Deploy scheduled tasks on AWS EC2 instances
- Use `.env` to manage environment variables

## Local Setup

Clone the repo, go to the repo folder, setup the virtual environment, and install the required packages:

```
cd send-me-eth
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

You then need to create a `.env` file in the project folder and add the following lines:

```
WALLET_ADDRESS='your wallet address'
SENDGRID_API_KEY='your sendgrid api key'
FROM_EMAIL='your sendgrid from email'
TO_EMAIL='the email you want to send notification to'
```

Then, run `python send-me-eth.py` every 24 hours to get 0.1 eth each time.

## Deploy to AWS EC2

I also show how to deploy the script on AWS EC2 as a scheduled task.

Create an AWS EC2 Ubuntu instance:

- Ubuntu 20.04 (x86)
- t2.micro (free tier)
- security group with SSH port 22 inbound enabled - outbound default all open
- create a new RSA key pair - download the .cer file

SSH to the remote instance, switch to the folder with the `.cer` file:

```
chmod 400 aws-gmail.cer
ssh -i "aws-gmail.cer" ubuntu@ec2-54-227-212-97.compute-1.amazonaws.com
```

From the remote Ubuntu prompt:

```
git clone https://github.com/harrywang/send-me-eth.git
cd send-me-eth/
```

Then create a `.env` file (see above) 

```
vim .env  # create .env file
ubuntu@ip-172-31-82-22:~/send-me-eth$ ls
LICENSE  README.md  requirements.txt  send-me-eth.py
```

Then, install/upgrade required packages (Python 3.8.10 is the default):
```
python3 --version
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
pip3 install --upgrade requests
```

You need to manually install Chrome:

```
sudo apt install wget
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get install -f  # run this if run into problem installing chrome next
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

Now, you can test the script by running `python3 send-me-eth.py` - you should receive an email. 

Next, use `crontab` to schedule the task (FYI: the word “Cron” comes from the Greek word “Chronos” (time), and `crontab` stands for “Cron table”).

A cron schedule expression has five fields: minute, hour, day of month, month, day of week

You can use https://crontab.guru/ to edit the expression. For example: `*/1 * * * *` means running task every minute and `5 */24 * * *` means running task at minute 5 past every 24th hour.

Check the path of our default python and our script:

```
which python3
/usr/bin/python3
pwd
/home/ubuntu/send-me-eth
```

Now, run `crontab -e` to add the following line to the file (I choose vim as the editor), save the file (press ESC, then type `:wq`) and you have scheduled a task.

`*/1 * * * * /usr/bin/python3 /home/ubuntu/send-me-eth/send-me-eth.py`

Use `crontab -l` to check the running task:

```
$ crontab -l
*/1 * * * * /usr/bin/python3 /home/ubuntu/send-me-eth/send-me-eth.py
```

Now, you should get an email every minute as a test. 

Finally, you can change the task to run at minute 5 past every 24th hour:

`5 */24 * * * /usr/bin/python3 /home/ubuntu/send-me-eth/send-me-eth.py`

Now, you can close the terminal and automatically get 0.1 eth every day :). Make sure to delete the cron task when you get enough testing ether.