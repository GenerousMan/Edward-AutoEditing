# 飞影 Cut Mins - 算法后端

> 备注：该README中说明的路径，除非特别指定，都是以`algrithm-center`作为根目录。

算法后端使用的框架是`Flask`，一个简洁的基于`Python`的API框架，用于桥接使用python实现的绝大部分剪辑相关的算法。

## 文件组织

- `edit`：剪辑算法模块，具体的细节由该算法模块的`README`说明；
- `routes`：算法接口路由组件，用路径来区分管理不同平台的接口；
    - `exhibit.py`：新版本系统添加的接口；
    - `video_cloth_ads.py`：旧版本系统的接口；
- `src`：`torchsample`的安装需求文件，暂时搁置没有管；
- `temp`：一些临时生成文件的保存位置；
    - `project`：用户自定义剪辑任务的临时环境保存位置；
- `.gitignore`：用于忽略目录下一些文件的git配置文件；
- `app-old.py`：非常旧版本的接口和启动程序，暂时搁置不管；
- `app.py`：新版本的启动程序；
- `examples.py`：用来预处理示例素材的脚本；
- `locks.py`：算法后端的全局GPU锁，避免多进程资源占用冲突；
- `process.json`：用于`pm2`进程管理工具的配置文件，在部署或调试的时候会使用到；
- `env-ubuntu.yaml`：当前版本在`Ubuntu 16.04`环境下的`conda`虚拟环境依赖文件。

## 环境要求

- `conda`：`miniconda` or `anaconda`，较新的版本即可；
- `os`：建议使用`ubuntu 16.04`，其他环境的虚拟环境文件不一定会有；
- `pm2`：一个进程管理工具，用于在web服务崩溃后自动重启。

## 开始

如果你是第一次运行该项目，这意味着你很可能没有对应的`conda`环境，先下载对应操作系统版本的`yaml`，然后在该目录下进入命令行。

```bash
conda env create -f <file_name>.yaml
// conda env create -f env-ubuntu.yaml
```

如果是在版本变动后重新运行，请先通过`env`目录下的对应操作系统的`.yaml`文件更新你的`conda`环境。

```bash
conda activate <your_old_conda>
conda env update --file <file_name>.yaml
// conda env update --file env-ubuntu.yaml
```

如果没有安装`pm2`工具，请先安装，如果安装过程出现问题请参考[官方文档](https://pm2.keymetrics.io/)。

```bash
npm install pm2 -g
```

### 调试

`Flask`在调试的时候也不支持热加载，所以使用了`pm2`的`watch`功能，它会在监视到文件变化后重启`Flask`进程，这些配置在`process.json`中已经编写，基本上不需要修改，默认的服务端口是`5050`，在`app.py`文件中可以修改端口，如果需要修改并且后端也是在调试时，请一并修改`Express`的算法端端口设置（在`{平台根目录}/api-center/routes/edit.js`文件的第19行代码：`var algorithm_port = 5050;`）。

```bash
pm2 start process.json
```

查看pm2中在运行的进程：

```bash
pm2 list
```

查看pm2中运行程序的输出：

```bash
pm2 log algrithm-center-exhibit
```

其他操作：

```bash
# 停止指定进程
pm2 stop algrithm-center-exhibit
# 停止所有进程
pm2 stop all
```

```bash
# 重启指定进程
pm2 restart algrithm-center-exhibit
# 重启所有进程
pm2 restart all
```

```bash
# 删除指定进程
pm2 delete algrithm-center-exhibit
# 删除所有进程
pm2 delete all
```

> 2021/01/06 by YuMi