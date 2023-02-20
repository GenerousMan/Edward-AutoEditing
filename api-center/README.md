# 飞影 Cut Mins - 数据后端

> 备注：该README中说明的路径，除非特别指定，都是以`api-center`作为根目录。

数据后端框架`Express.js`，虽然前端工程从后端中分离出去了，但是还是使用了和前端框架有较高契合度的语言，便于开发者维护；并且基于`Node.js`的`Express`能够在简单的维护下提供较高的并发性能。

## 文件组织

- `bin/www`：`Express`运行脚本；
- `node_modules`：使用命令`npm install`后，包含所有运行依赖包；
- `public`：后端的`public`可访问文件目录；
    - `css`：旧版系统的css文件合集，不再展开说明；
    - `examples`：示例素材的存放位置，可以被页面访问；
    - `img`：旧版和新版系统的所有图片素材存放；
    - `js`：旧版系统的js文件合集，不再展开说明；
    - `media`：新版系统的所有视频素材存放；
    - `tempoFiles`：存放一些临时生成的文件；
        - `thumbnails`：存放生成的封面图片；
            - `.gitignore`：用于忽略目录下的文件但保留目录；
        - `videos`：存放生成的视频文件；
            - `.gitignore`：用于忽略目录下的文件但保留目录；
    - `tools`：旧版系统的各种依赖文件缓存，避免加载卡顿；
    - `videos`：所有案例视频存放位置，每个案例包含一系列镜头的帧图片以及一个视频文件；
    - `vue-css`：来自前端`vue`打包后的`dist/css`目录，存放页面样式文件。
    - `vue-js`：来自前端`vue`打包后的`dist/js`目录，存放页面的脚本文件;
    - `exhibit.html`：来自前端`vue`打包后的`dist/index.html`文件；
    - `favicon.ico`：来自前端`vue`打包后的`dist/favicon.ico`文件，页面tab的图标
- `routes`：旧版系统的各路由模块文件，在`app.js`中导入；
    - `edit.js`：剪辑接口的路由文件；
    - `index.js`：主接口的路由文件（暂时没怎么使用）；
- `views`：`Express`的页面视图文件，旧版系统中所有的视图页面文件，不再展开说明；
- `.gitignore`：用于忽略一些不必要的文件；
- `app.js`：`Express`主程序，在运行脚本中会被引入并启用；
- `package.json`：`Express`依赖的一些包的管理配置文件；
- `dev.json`：用于`pm2`进程管理工具的配置文件，在调试的时候会使用到；
- `product.json`：用于`pm2`进程管理工具的配置文件，在部署的时候会使用到。

## 环境要求

- `node.js`：比较新的LTS版本就好。
- `npm`：在`node`安装包里顺带安装。
- `os`：操作系统基本上各个都OK，`node`都能够跑。
- `pm2`：一个进程管理工具，因为`node`原本的`HTTP Server`是单进程的，一旦崩溃后无法自己重启；`pm2`可以维护`node`进程，崩溃后自动重启等操作（其实也可以管理其他环境和语言的进程，例如`Python`等）。

## 开始

如果你是第一次运行该项目（或者是克隆来的项目，尤其是没有`node_modules`文件夹），请先在`api-center`目录下执行包安装命令，包会安装到`node_modules`目录下，这一般会需要个几分钟，取决于网络情况，如果出现安装失败的包，请酌情处理。

```bash
npm install
```

注：`node_modules`目录已经在`.gitignore`中设置为不跟踪，所以里面的包不会被上传。

如果没有安装`pm2`工具，请先安装，如果安装过程出现问题请参考[官方文档](https://pm2.keymetrics.io/)。

```bash
npm install pm2 -g
```

## 调试

`Express`在调试的时候并不支持热加载，所以需要使用`pm2`对路由接口文件进行监视`watch`，这些配置在`dev.json`中已经编写，基本上不需要修改，默认的服务端口是`4000`，在`bin/www`文件中可以修改端口，如果需要修改并且前端页面也是在调试时，请一并修改`vue`前端的`vue.config.js`中的代理端口设置。

```bash
pm2 start dev.json
```

查看pm2中运行程序的输出：

```bash
pm2 log api-center-exhibit
```

其他操作：

```bash
# 停止指定进程
pm2 stop api-center-exhibit
```

```bash
# 重启指定进程
pm2 restart api-center-exhibit
```

```bash
# 删除指定进程
pm2 delete api-center-exhibit
```

## 部署

部署时不会再去监视文件修改而重启，默认的服务端口是`4000`。

```bash
pm2 start dev.json
```

> 2021/01/06 by YuMi