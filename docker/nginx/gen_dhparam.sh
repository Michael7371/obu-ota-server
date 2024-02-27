function main() {
    echo_params | openssl dhparam -out /etc/nginx/dhparam.pem 2048

    service nginx restart
}

main