# Edward - Data Backend

> Remarks: The paths described in the README, unless otherwise specified, use `api-center` as the root directory.

The data back-end's framework is `Express.js`. Although the front-end project is separated from the back-end, it still uses a language that has a high degree of fit with the front-end framework, which is convenient for developers to maintain. It based on `Node.js` 's `Express`, which can provide high concurrency performance with simple maintenance.

## File organization

- `bin/www`: `Express` run script;
- `node_modules`: After using the command `npm install`, it contains all running dependencies;
- `public`: the `public` accessible file directory of the backend;
     - `css`: a collection of css files of the old version system, no more descriptions;
     - `examples`: the storage location of the example material, which can be accessed by the page;
     - `img`: storage of all image materials of the old and new versions of the system;
     - `js`: a collection of js files of the old version system, no more descriptions;
     - `media`: storage of all video materials of the new system;
     - `tempoFiles`: store some temporarily generated files;
         - `thumbnails`: store the generated cover image;
             - `.gitignore`: used to ignore files under the directory but keep the directory;
         - `videos`: store generated video files;
             - `.gitignore`: used to ignore files under the directory but keep the directory;
     - `tools`: Various dependent file caches of the old system to avoid loading lag;
     - `videos`: storage location of all case videos, each case contains frame pictures of a series of shots and a video file;
     - `vue-css`: from the `dist/css` directory packaged by the front-end `vue`, storing page style files.
     - `vue-js`: from the `dist/js` directory packaged by the front-end `vue`, storing the script files of the page;
     - `exhibit.html`: from the `dist/index.html` file packaged by the front-end `vue`;
     - `favicon.ico`: From the `dist/favicon.ico` file packaged by the front-end `vue`, the icon of the page tab
- `routes`: each routing module file of the old system, imported in `app.js`;
     - `edit.js`: the routing file of the clipping interface;
     - `index.js`: the routing file of the main interface (not used much for now);
- `views`: the page view file of `Express`, all the view page files in the old system, no more description;
- `.gitignore`: used to ignore some unnecessary files;
- `app.js`: `Express` main program, which will be imported and enabled in the running script;
- `package.json`: the management configuration file for some packages that `Express` depends on;
- `dev.json`: configuration file for `pm2` process management tool, which will be used during debugging;
- `product.json`: The configuration file for the `pm2` process management tool, which will be used during deployment.

## Environmental requirements

- `node.js`: A newer LTS version is fine.
- `npm`: installed incidentally in the `node` installation package.
- `os`: Basically all operating systems are OK, and `node` can run.
- `pm2`: a process management tool, because the original `HTTP Server` of `node` is a single process, once it crashes, it cannot restart itself; `pm2` can maintain the `node` process, automatically restart after a crash, etc. (actually It is also possible to manage processes in other environments and languages, such as `Python`, etc.).

## start

If you are running this project for the first time (or a cloned project, especially if there is no `node_modules` folder), please execute the package installation command in the `api-center` directory first, and the package will be installed to the `node_modules` directory Normally, it will take a few minutes, depending on the network conditions. If there is a package that fails to install, please handle it accordingly.

```bash
npm install
```

Note: The `node_modules` directory has been set as untracked in `.gitignore`, so packages inside it will not be uploaded.

If the `pm2` tool is not installed, please install it first. If there is a problem during the installation process, please refer to [Official Documentation](https://pm2.keymetrics.io/).

```bash
npm install pm2 -g
```

## debug

`Express` does not support hot loading during debugging, so you need to use `pm2` to monitor the routing interface file `watch`, these configurations have been written in `dev.json`, basically do not need to be modified, the default service The port is `4000`, you can modify the port in the `bin/www` file, if you need to modify and the front-end page is also debugging, please modify the proxy port settings in `vue.config.js` in the `vue` front-end .

```bash
pm2 start dev.json
```

View the output of running the program in pm2:

```bash
pm2 log api-center-exhibit
```

Other operations:

```bash
# Stop the specified process
pm2 stop api-center-exhibit
```

```bash
# Restart the specified process
pm2 restart api-center-exhibit
```

```bash
# delete the specified process
pm2 delete api-center-exhibit
```

## deployment

When deploying, it will no longer monitor file modification and restart. The default service port is `4000`.

```bash
pm2 start dev.json
```
