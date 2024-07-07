# geek-camp-vol8

## 技育 CAMP vol.8 でのチーム開発リポジトリ
## Install
### With Docker
```shell
docker pull kamesan1577/discord-memo:latest
docker run --env DISCORD_TOKEN="your_discord_token" kamesan1577/discord-memo:latest 
```
または
```shell
git clone --depth 1 https://github.com/kamesan1577/geek-camp-vol8.git
cd geek-camp-vol8 && cp .env.sample .env
vim .env # discord bot tokenを記述する
docker compose build
docker compose up
```
