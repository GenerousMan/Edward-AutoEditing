# 飞影 Cut Mins - 前端页面

> 备注：该README中说明的路径，除非特别指定，都是以`vue-app`作为根目录。

在展厅版本系统，分支`v0.3-exhibit`，引入单独的前端页面项目，用以开发更加具有交互性的页面，同时让页面之间的过渡更加自然。前端页面使用框架`Vue.js`，语言`JavaScript`，编译环境依赖`node.js`、`npm`。

## 文件组织

- `dist`：使用命令`npm run build`后会生成的打包文件夹，包含所有页面文件；
- `node_modules`：对于克隆项目，使用`npm install`后会生成的运行时依赖环境文件夹，包含所有运行依赖包；
- `public`：基础页面文件；
- `src`：绝大部分源代码和资源；
    - `assets`：图片、视频等静态资源；
    - `components`：所有`Vue`模块组件代码；
        - `Exhibit.vue`：首页组件；
        - `Loading.vue`：Loading等待窗口组件；
        - `Results.vue`：结果页组件；
        - `Select.vue`：功能选择页面组件；
        - `Upload.vue`：上传素材页面组件；
        - `Videos.vue`：示例素材选择页面组件；
        - `Wait.vue`：进度等待页面组件；
    - `App.vue`：主APP组件；
    - `main.js`：主程序代码，内部包含页面路由和组件引入；
- `.gitignore`：git仓库管理范围的配置文件；
- `babel.config.js`：Babel相关的配置文件，一般不会修改；
- `package.json`：第三方依赖包管理；
- `vue.config.js`：Vue的一些额外配置，这里使用到了调试代理设置。

## 开始

第三方依赖环境都在`package.json`中，如果是克隆的项目，是不包含运行时文件夹`node_modules`的，此时需要在`vue-app`文件夹下执行安装依赖环境的命令：

```bash
npm install
```

## 环境要求

- `node.js`：比较新的LTS版本就好；
- `npm`：在`node`安装包里顺带安装。

## 调试

`Vue.js`框架一般用于开发单页面应用，为了可以更加方便地编码和调试，前端在调试时，是使用一套单独的运行时来管理的，即不需要依赖其他服务器就可以开发页面代码。

启动调试模式的命令：

```bash
npm run serve
```

根据命令执行成功后提示的端口访问页面，调试的时候也可以对接其他服务器的接口，相关配置在`vue.config.js`文件中，其中的配置可以启用一个代理服务，让前端页面的指定HTTP请求转发到指定端口的服务器，从而在数据互通的情况下开发和调试。

## 部署

部署时，使用命令：

```bash
npm run build
```

执行成功后，会将结果文件打包放在`dist`文件夹下：

- `css`，请手动修改为`vue-css`；
- `img`；
- `js`，请手动修改为`vue-js`；
- `favicon.ico`；
- `index.html`，请手动修改为`exhibit.html`。

在`index.html`(或修改后的`exhibit.html`)中，将所有`/css/`修改为`/vue-css/`，将所有`/js/`修改为`/vue-js/`。

然后将以上所有文件，复制到`{平台根目录}/api-center/public`下（除了`img`的其他同名文件或文件夹请删除）。

> 2021/01/05 by YuMi