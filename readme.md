# Nginx reverse proxy with load balancing + setup SSL/TLS simple example
References:
* [reference 1](https://www.digitalocean.com/community/tutorials/openssl-essentials-working-with-ssl-certificates-private-keys-and-csrs)
* [reference 2](https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-on-centos-7)
* [reference 3](https://docs.joshuatz.com/cheatsheets/security/self-signed-ssl-certs/)
* [SAN issue on windows](https://stackoverflow.com/questions/43665243/invalid-self-signed-ssl-cert-subject-alternative-name-missing)
## Self-signed certificate
* Setup self-signed ssl certificate:
    * Create a self-signed key and certificate pair:
        * Generate a private key and certificate signing request (CSR)
        ```
        sudo openssl req -newkey rsa:2048 -nodes -keyout tls/nginx-selfsigned.key -out tls/nginx-selfsigned.csr -config csr.conf
        ```
        * Generate a self-signed certificate from private key and CSR
        ```
        sudo openssl x509 -signkey tls/nginx-selfsigned.key -in tls/nginx-selfsigned.csr -req -days 365 -out tls/nginx-selfsigned.crt
        ```
        * 2-in-1: Create a private key and self-signed certificate
        ```
        sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls/nginx-selfsigned.key -out tls/nginx-selfsigned.crt -config crt.conf
        ```
    * Mount `nginx-selfsigned.crt` and `nginx-selfsigned.key` into nginx container
* Deploy: `docker compose up -d`
* Test connection
    * (For ubuntu) Install certificate
    ```
    sudo cp tls/nginx-selfsigned.crt /usr/local/share/ca-certificates
    sudo update-ca-certificates --fresh
    ```
    * Add the following entry in `/etc/hosts`
    ```
    127.0.0.1       tenmien.site
    ```
    * Test with curl
    ```
    curl https://tenmien.site/path1
    ```
## Getting certificate from Let's Encrypt manually with certbot
* References:
    * [reference 1](https://community.letsencrypt.org/t/my-server-provided-me-csr-to-get-ssl-from-letsencrypt/152371/4)
    * [reference 2](https://letsencrypt.org/docs/challenge-types/#dns-01-challenge)
* Purchase a domain name from a domain registrar (e.g. namecheap)
* Generate a private key and certificate signing request (CSR)
```
sudo openssl req -newkey rsa:2048 -nodes -keyout tls/domain.key -out tls/domain.csr -config csr.conf
```
* Getting certificate
    * Run a certbot container
    ```
    docker run -it --rm -v `pwd`/tls:/tls --entrypoint "/bin/sh" certbot/certbot
    ```
    * Manually obtain a certificate from Let's Encrypt with a CSR file and validate domain ownership using DNS records
    ```
    cd /tls
    certbot certonly --manual --csr domain.csr --preferred-challenges dns-01 --register-unsafely-without-email
    ```
    * Complete DNS challenge: create a DNS TXT record to complete the challenge
    ![DNS challenge](assets/dns_challenge.png "Create a txt record to complete the dns challenge")
    * Obtain 3 files `0000_cert.pem`, `0000_chain.pem` and `0001_chain.pem` -> use `0001_chain.pem` for certificate file
    * Mount `0001_chain.pem` and `domain.key` into nginx container
* Deploy: `docker compose up -d`
* Test connection
    * Create a DNS A record to map domain to local IP
    * Test with curl
    ```
    curl https://tenmien.site/path1
    ```

TODO: certbot to auto renew certificate, cert-manager for k8s ingress