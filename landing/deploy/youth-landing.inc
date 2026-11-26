    location = /youth-station { return 308 /youth-station/; }
    location = /youth-station/ { rewrite ^ /youth-station/index.html last; }
    location = /youth-station/index.html {
        internal;
        alias /usr/share/nginx/html/youth-station/index.html;
        default_type text/html;
        add_header Cache-Control "no-cache";
    }
    location ~ ^/youth-station/(?<youth_json>public-stats\.json|android-release\.json)$ {
        alias /usr/share/nginx/html/youth-station/$youth_json;
        default_type application/json;
        add_header Cache-Control "no-store" always;
        add_header X-Content-Type-Options "nosniff" always;
    }
    location ~ ^/youth-station/(?<youth_apk>youth-station-android-[a-zA-Z0-9][a-zA-Z0-9._-]*\.apk)$ {
        alias /usr/share/nginx/html/youth-station/$youth_apk;
        default_type application/vnd.android.package-archive;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Content-Disposition "attachment";
    }
    location /youth-station/ { return 404; }
