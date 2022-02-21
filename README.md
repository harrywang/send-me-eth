# About
a simple automated tool to get testing ether from https://www.rinkebyfaucet.com/

## Setup

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

Then, run `python send-me-eth.py` every 24 hours to get 0.1 eth from https://www.rinkebyfaucet.com/