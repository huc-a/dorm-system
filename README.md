# 基于 Spring Boot + Vue 的宿舍管理系统

毕业设计项目：前后端分离的高校宿舍管理系统，配套毕业论文见 `docs/` 目录。

## 技术栈

- 后端：Java 21、Spring Boot 3.3.5、Spring Security + JWT、Spring Data JPA、MySQL 8.0、springdoc-openapi（Swagger）
- 前端：Vue 3、Element Plus、Pinia、Vue Router、Axios、ECharts、Vite

## 功能模块

学生管理、宿舍楼管理、房间管理、床位管理、入住管理（入住分配 / 调宿 / 退宿，含床位占用与重复入住校验）、报修管理、卫生检查、访客登记、水电费管理、请假/晚归审批、通知公告、仪表盘统计（入住率、各楼栋入住、报修状态、最新公告）、学生自助（我的宿舍：在线报修、请假申请、费用查询）、学生自助注册、系统账号管理（仅管理员：建号、禁用、重置密码）。

三类角色：系统管理员（ADMIN）、宿舍管理员（DORM_MANAGER）、学生（STUDENT）。

## 目录结构

```
dorm-system/
├── backend/            Spring Boot 后端（48 个 Java 源文件，12 张数据表对应实体）
├── frontend/           Vue 3 前端（配置驱动的通用 CRUD 页面 + 仪表盘 + 学生端）
├── sql/schema.sql      数据库建表语句（由实际数据库导出）
├── docs/               毕业论文（docx/pdf）、论文插图、论文生成脚本
├── .env                数据库连接配置（DB_USERNAME / DB_PASSWORD，权限 600，勿提交公开仓库）
└── README.md
```

## 运行方式

当前已在本机以 systemd 服务 `dorm-app` 运行（开机自启，依赖 `mysql` 服务）。应用默认端口为 8081（application.yml），现通过服务环境变量 `SERVER_PORT=8080` 改在 8080 运行，以匹配 Cloudflare 隧道既有路由，并已对外发布：

- 公网地址：https://muse-tunnels.453.de5.net/ （Cloudflare 隧道 Muse-Test，路由 HTTP → localhost:8080）
- 本地地址：http://127.0.0.1:8080/
- 接口文档：http://127.0.0.1:8080/swagger-ui/index.html
- 服务管理：`systemctl status|restart dorm-app`，日志 `journalctl -u dorm-app -f`

从源码重新构建：

```bash
# 1. 数据库：创建库与账号（密码见 .env）
mysql -u root -e "CREATE DATABASE dorm_db CHARACTER SET utf8mb4;"
# 2. 前端构建并放入后端静态资源
cd frontend && npm install && npm run build
cp -r dist/* ../backend/src/main/resources/static/
# 3. 后端打包运行（Java 启动需加 -Djava.net.preferIPv4Stack=true，本机网络特性要求）
cd ../backend && mvn -DskipTests package
DB_USERNAME=dorm DB_PASSWORD=<见.env> java -Djava.net.preferIPv4Stack=true -jar target/dorm-system-1.0.0.jar
```

首次启动会自动初始化演示数据（账号、2 栋楼、24 间房、96 个床位、12 名学生、10 条入住记录等）；数据库已有用户数据时自动跳过。

前端开发模式：`cd frontend && npm run dev`（端口 5174，已配置 /api 代理到 8081）。

## 演示账号

| 角色 | 用户名 | 密码 |
| --- | --- | --- |
| 系统管理员 | admin | admin123 |
| 宿舍管理员 | manager | manager123 |
| 学生 | 20230101（学号） | 123456 |

其余演示学生账号为各自学号（20230102…20230206），密码均为 123456。

## 毕业论文

`docs/基于SpringBoot+Vue的宿舍管理系统的设计与实现-毕业论文.docx`（另附同名 PDF 预览版）。
全文约 2 万字、37 页，含摘要/Abstract、7 章正文、4 幅插图（架构图、功能模块图、E-R 图、入住流程图）、19 张表格（12 张数据表结构、接口表、测试用例表等）与 16 条参考文献。
使用前请将封面与独创性声明中的学校、学院、专业、姓名、学号、指导教师等占位信息替换为本人真实信息，并按学校模板要求调整格式、在 Word 中生成带页码的自动目录。
