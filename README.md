# Edward(飞影/Cut Mins) - Automatic Reference-Based Video Editing with Pose Style Transfer

![image](https://github.com/GenerousMan/Edward-AutoEditing/blob/master/api-center/public/img/System.jpg)

## Platform overview

**Edward(飞影/Cut Mins)**. Current version is designed to display in the exhibition hall. We have made a lot of optimization in the interaction. The core function is not changed much compared with the previous version in the paper. To simplify the content of the system, no customized modification function has been added to the new version of the interface, but the old version of the system (including editing customized modification) can still be accessed in the code of this version. Most interfaces share the same set of APIs with the new system. But because the algorithm backend only occupies one GPU, the new and old platforms will share a GPU lock when using the algorithm backend API at the same time, causing one side to wait.

- New version platform access URL: `http://<ip>:<port>/exhibit.html#/exhibit`；
- Old version platform access URL: `http://<ip>:<port>/edit/video-cloth-ads/upload`。

If you run this platform locally, `ip` can be `localhost` or `127.0.0.1`，and the `port` is `4000`; When bridging to the external network, fill in the server's external network IP and corresponding mapping port.

The new platform architecture is divided into three parts:

- **Front Page**：In the folder `vue-app`, which is used to develop the interactive interface of the new system. The developing framework is `Vue.js`, with the language `JavaScript`；
- **Data Backend**：In the folder`api-center`. As an intermediate layer, pull out some interfaces that do not need to use algorithms here, improve the efficiency of page data access, and also facilitate the development and debugging separately from the algorithm side, or expand the concurrency requirements of the multi-algorithm backend in the future. Using the framework `express. js`, language `JavaScript`, and database `mongodb`;
- **Algorithm Backend**：in the folder `algrithm-cneter`, which contains interfaces those realize the core functions of our algorithms. It uses the framework `Flask`, and language `Python`(3.6).

There are separate `README. md` documents under subfolders to explain more details. This document will only describe some major version changes later.

## Files Organization Structure

- `algrithm-cneter`：Algorithm Backend;
- `api-center`：Data Backend;
- `dump`：Mongodb database export data backup;
- `examples`：Store backup of sample material;
- `match-results`：Store the case matching results of algorithm execution;
- `templates`：Store all case videos;
- `uploads`：Store all uploaded video materials;
- `vue-app`：Front pages.

## Deployment

**Please ensure that each module can run smoothly before deployment**，Because `pm2` is used to manage the running of all service processes, please ensure that `node. js`, `npm`, `pm2`and other environments have been installed before deployment.

### 1 Packaging front end

Execute the packaging command in the `vue-app` directory:

```bash
npm run build
```

The packaged file will be in the generated 'vue-app/list' directory:

- `css`, please manually change to `vue-css`;
- `img`;
- `js`, please manually change to `vue-js`;
- `favicon.ico`;
- `index. html`, please manually change it to `exhibit. html`.

In `index. html` (or modified `exhibit. html`), change all `/css/` to `/vue css/` and all `/js/` to `/vue js/`.

Then copy all the above files to ` api-center/public '(delete other files or folders with the same name except ` img').

### 2 Start the Database

In any directory, execute the command:

```bash
sudo mongod --dbpath=/var/lib/mongodb --logpath=/var/log/mongodb/mongod.log
```

The parameters of `dbpath` and `logpath` in the command are set according to the server environment. Here is only an example. It is recommended to use a `screen` for management, or register `mongodb` as a background service by referring to the official document (you don't need to enter the above command to hang a process).

### 3 Start the Data Backend

In the folder `api-center`, run the following command:

```bash
pm2 start product.json
```

The data backend is deployed on the `4000` port by default. If you want to modify it, please modify it in the `api-center/bin/www` file.

### 4 Start the Algorithm Backend

In the `algrithm-center` directory, execute the startup command (please ensure that you have switched to the specified `conda` environment):

```bash
pm2 start process.json
```

The algorithm backend is deployed on the `5050` port by default. If you want to modify it, please modify it in the `algrithm-center/app.py` file.