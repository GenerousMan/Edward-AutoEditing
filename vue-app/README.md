# Edward - front page

> Remarks: The paths described in the README, unless otherwise specified, use `vue-app` as the root directory.

In the exhibition hall version system, this branch introduces a separate front-end page project to develop more interactive pages and make the transition between pages more natural. The front-end page uses the framework `Vue.js`, the language `JavaScript`, and the compilation environment depends on `node.js` and `npm`.

## File organization

- `dist`: The packaging folder that will be generated after using the command `npm run build`, including all page files;
- `node_modules`: For cloned projects, the runtime dependent environment folder will be generated after using `npm install`, including all runtime dependent packages;
- `public`: base page file;
- `src`: most of the source code and resources;
     - `assets`: Static resources such as pictures and videos;
     - `components`: all `Vue` module component codes;
         - `Exhibit.vue`: Home page component;
         - `Loading.vue`: Loading waits for window components;
         - `Results.vue`: result page component;
         - `Select.vue`: function selection page component;
         - `Upload.vue`: upload material page component;
         - `Videos.vue`: sample material selection page component;
         - `Wait.vue`: progress waiting page component;
     - `App.vue`: main APP component;
     - `main.js`: the main program code, which contains page routing and component introduction;
- `.gitignore`: configuration file for git warehouse management scope;
- `babel.config.js`: Babel-related configuration files, generally not modified;
- `package.json`: Third-party dependency package management;
- `vue.config.js`: Some additional configurations of Vue, where the debugging proxy settings are used.

## start

The third-party dependent environment is in `package.json`. If it is a cloned project, it does not include the runtime folder `node_modules`. In this case, you need to execute the command to install the dependent environment in the `vue-app` folder:

```bash
npm install
```

## Environmental requirements

- `node.js`: A newer LTS version is fine;
- `npm`: installed incidentally in the `node` installation package.

## debug

The `Vue.js` framework is generally used to develop single-page applications. In order to facilitate coding and debugging, the front-end is managed by a separate runtime when debugging, that is, pages can be developed without relying on other servers code.

Command to start debug mode:

```bash
npm run serve
```

According to the port access page prompted after the command is successfully executed, you can also connect to the interface of other servers during debugging. The relevant configuration is in the `vue.config.js` file. The configuration in it can enable a proxy service to allow the specified HTTP on the front-end page The request is forwarded to the server at the specified port, so as to develop and debug under the condition of data communication.

## deployment

When deploying, use the command:

```bash
npm run build
```

After the execution is successful, the result file will be packaged and placed in the `dist` folder:

- `css`, please manually modify it to `vue-css`;
- `img`;
- `js`, please manually modify it to `vue-js`;
- `favicon.ico`;
- `index.html`, please manually modify it to `exhibit.html`.

In `index.html` (or modified `exhibit.html`), change all `/css/` to `/vue-css/` and all `/js/` to `/vue-js /`.

Then copy all the above files to `{platform root directory}/api-center/public` (please delete other files or folders with the same name except `img`).