# 青年驿站宣传页

`index.html` 为宣传页本体。生产页面从同目录读取 `public-stats.json` 和 `android-release.json`，不直连数据库。统计初次读取失败时不显示伪造数字；后台每约 30 秒汇总，页面每 60 秒刷新一次。演示送达数单独标注。

`deploy/` 内是 Linux 部署模板：将静态页放在 `/usr/share/nginx/html/youth-station/`，并在现有 HTTPS 虚拟主机内引入 Nginx 配置。部署 Python 脚本与 systemd 服务及计时器前，请设定对应目录、数据库名，以及服务器上的只读 MySQL 客户端配置；账户仅需查询学生、骑手、驿站和代取订单四张表，配置文件不可放进网页目录。启用前用 `nginx -t` 检查配置。

完整 APK 需要另行发布。将 `android-release.example.json` 作为清单格式参考，确认 APK 可下载且校验值正确后，再更新实际的 `android-release.json`。详见 `android-release-guide.md`。本目录不包含 APK、数据库导出或凭据。
