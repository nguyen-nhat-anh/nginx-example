## Nginx reverse proxy + load balance simple example
* Test connection
```
curl -H "Host: example.com" https://localhost/path1
```
* Setup self-signed ssl certificate ([reference 1](https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-on-centos-7), [reference 2](https://docs.joshuatz.com/cheatsheets/security/self-signed-ssl-certs/), [SAN issue on windows](https://stackoverflow.com/questions/43665243/invalid-self-signed-ssl-cert-subject-alternative-name-missing)):
    * Create a self-signed key and certificate pair:
    ```
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx-selfsigned.key -out nginx-selfsigned.crt -config openssl.conf
    ```
    * Fill out the prompts. **The most important line is the one that requests the Common Name (e.g. server FQDN or YOUR name). You need to enter the domain name associated with your server or your server’s public IP address.**
    ```
    Common Name (eg, your name or your server's hostname) []: example.com
    ```
    * Mount `nginx-selfsigned.crt` into `/etc/ssl/certs` directory and mount `nginx-selfsigned.key` into `/etc/ssl/private` directory inside nginx container
* TODO: certbot to auto renew certificate, ssl/tls for k8s ingress