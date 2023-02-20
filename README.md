# 飞影 Cut Mins

## 平台概况

**飞影(Cut Mins)**，当前版本分支`v0.3-exhibit`，原本的初衷是做成可以在展厅展示的系统版本，所以在交互上做了较多的优化，最后的核心功能相较于之前的版本并没有太大的变化，为了简化系统的内容，暂时没有在新版界面中加入自定义修改的功能，但旧版的系统（包括剪辑自定义修改），在本版代码中仍可以继续访问，并且后台功能正常运行，大部分接口和新版系统共享同一套API，但因为算法后端只占用一个GPU，所以新旧平台在同时使用算法后端的API时会共享一个GPU锁，导致其中一方等待。

- 新版平台访问URL：`http://<ip>:<port>/exhibit.html#/exhibit`；
- 旧版平台访问URL：`http://<ip>:<port>/edit/video-cloth-ads/upload`。

如果在本地运行，访问的`ip`可以填写`localhost`或者`127.0.0.1`，`port`为`4000`；桥接映射到外网时，填写服务器的外网IP和对应的映射端口即可。

新版的平台架构分为三块：

- **前端页面**：文件夹`vue-app`，用于开发新版系统的交互界面，前端框架`Vue.js`，语言`JavaScript`；
- **数据后端**：文件夹`api-center`，作为一个中间层，将一些不需要使用到算法的接口抽离到这里，提高页面数据访问的效率，同时也便于和算法端分离地开发调试，或者未来拓展多算法后端的并发需求，使用框架`express.js`，语言`JavaScript`，数据库`mongodb`；
- **算法后端**：文件夹`algrithm-cneter`，实现算法核心功能的接口，使用框架`Flask`，语言`Python`(3.6)，以及其他算法依赖库。

在各级子文件夹下有单独的`README.md`文档来说明更加细节的内容，本文档后续仅说明一些比较大的版本变动。

## 文件组织

- `algrithm-cneter`：算法后端；
- `api-center`：数据后端；
- `dump`：mongodb数据库导出数据备份；
- `examples`：存放示例素材的备份；
- `match-results`：存放算法执行的案例匹配结果；
- `templates`：存放所有案例视频；
- `uploads`：存放所有上传视频素材；
- `vue-app`：前端页面。

## 部署步骤

**在部署前请确保各模块自身可以顺利运行**，由于是使用`pm2`来管理所有服务进程运行，所以请在部署前确保已经安装`node.js`、`npm`、`pm2`等环境。

### 1 打包前端

在`vue-app`目录下，执行打包命令：

```bash
npm run build
```

打包后的文件会在生成的`vue-app/dist`目录中：

- `css`，请手动修改为`vue-css`；
- `img`；
- `js`，请手动修改为`vue-js`；
- `favicon.ico`；
- `index.html`，请手动修改为`exhibit.html`。

在`index.html`(或修改后的`exhibit.html`)中，将所有`/css/`修改为`/vue-css/`，将所有`/js/`修改为`/vue-js/`。

然后将以上所有文件，复制到`api-center/public`下（除了`img`的其他同名文件或文件夹请删除）。

### 2 启动数据库

在任意目录下，执行命令：

```bash
sudo mongod --dbpath=/var/lib/mongodb --logpath=/var/log/mongodb/mongod.log
```

命令中的`dbpath`和`logpath`的参数根据服务器环境情况设定，这里只是列出一个使用示例，建议用一个`screen`来管理，或者参照官方文档将`mongodb`注册为一个后台服务（就不用再自己输入上述命令挂一个进程了）。

### 3 启动数据后端

在`api-center`目录下，执行启动命令：

```bash
pm2 start product.json
```

数据后端默认部署在`4000`端口，如果要修改，请到`api-center/bin/www`文件中修改。

### 4 启动算法后端

在`algrithm-center`目录下，执行启动命令（请先确保已切换到指定的`conda`环境下）：

```bash
pm2 start process.json
```

算法后端默认部署在`5050`端口，如果要修改，请到`algrithm-center/app.py`文件中修改。

> 2021/01/05 by YuMi