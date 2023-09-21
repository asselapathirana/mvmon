Deploying to a sub folder
1. Set the envioronmetal variable DASH_BASE_PATHNAME
dokku config:set rwh1 DASH_BASE_PATHNAME=/rwh1/
2. Set the directives in the nginx config: 
        location ~ ^/rwh1(.*) {
        proxy_set_header Host "rwh1.ws.environment.gov.mv";
        rewrite ^/rwh1(.*) /rwh1$1 break;
        proxy_pass http://localhost:80;
    }

