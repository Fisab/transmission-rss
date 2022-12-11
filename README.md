# transmission-rss

Service to check RSS and if regex match -> adding torrent to transmission
Docker image: ghcr.io/fisab/transmission-rss:master

`config.yml` example:
```yaml
rss_list:
  - url: https://api.anilibria.tv/v2/getRSS?rss_type=rss&limit=50
    download_dir: /volume1/tv/anime
    regex_group:
      must:
        - .*восхождение в тени!.*
      must_not:
        - hevc

transmission:
  username: user
  password: superpassword
  host: localhost
  port: 9091

database:
  file_name: rss.db

interval_check_rss: 300
```
`rss_list.regex_group.must` must found at feed title
`rss_list.regex_group.must_not` must not found at feed title
if both conditions above are met service will download torrent file (with type `application/x-bittorrent`) and add files which not seen before (caching at rss.db - `shelve`) to transmission

---

`docker-compose.yml` example:
```yaml
version: '3.3'
services:
  transmission_rss:
    image: ghcr.io/fisab/transmission-rss:master
    volumes:
      - ./config.yml:/src/config.yml:ro
      - ./internal:/src/internal:rw
    restart: always
```