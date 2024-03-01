# obu-ota-server
Nginx server to host firmwares for On Board Devices (OBU's)

## Setup
Make a copy of the `sample.env` file and rename it to `.env` with all relevenat variables filled out. After the .env is configured run `docker compose up` to spin up the nginx proxy and the fast api backend. 

## SSL Config
To run the nginx proxy with encryption, put your `.crt` and `.key` files in /docker/nginx/ssl. Update your .env file with the name of your `.crt` and `.key` files. Run the following command to spin up the docker containers: `docker compose -f docker-compose-ssl.yml up`
