# obu-ota-server
Nginx server to host firmwares for On Board Devices (OBU's)

## Setup
Make a copy of the `sample.env` file and rename it to `.env` with all relevenat variables filled out. After the .env is configured run `docker compose up` to spin up the nginx proxy and the fast api backend. 