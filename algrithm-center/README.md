# Edward - Algorithm Backend

> Remarks: The paths described in the README, unless otherwise specified, use `algrithm-center` as the root directory.

The framework used by the algorithm backend is `Flask`, a concise `Python`-based API framework, used to bridge most of the editing-related algorithms implemented in python.

## File organization

- `edit`: clipping algorithm module, the specific details are described in `README` of the algorithm module;
- `routes`: Algorithmic interface routing component, which uses paths to distinguish and manage interfaces of different platforms;
     - `exhibit.py`: the interface added by the new version system;
     - `video_cloth_ads.py`: the interface of the old version system;
- `src`: the installation requirement file of `torchsample`, temporarily put aside;
- `temp`: the storage location of some temporary generated files;
     - `project`: the temporary environment save location for user-defined editing tasks;
- `.gitignore`: git configuration file used to ignore some files in the directory;
- `app-old.py`: a very old version of the interface and launcher, which is left alone for now;
- `app.py`: the launcher for the new version;
- `examples.py`: scripts for preprocessing example assets;
- `locks.py`: the global GPU lock at the back end of the algorithm, to avoid conflicts of multi-process resource occupation;
- `process.json`: configuration file for `pm2` process management tool, which will be used when deploying or debugging;
- `env-ubuntu.yaml`: The current version of the `conda` virtual environment dependency file in the `Ubuntu 16.04` environment.

## Environmental requirements

- `conda`: `miniconda` or `anaconda`, the newer version is fine;
- `os`: It is recommended to use `ubuntu 16.04`, the virtual environment files of other environments may not have;
- `pm2`: a process management tool for automatically restarting web services after they crash.

## start

If you are running this project for the first time, it means that you probably do not have the corresponding `conda` environment, first download the `yaml` of the corresponding operating system version, and then enter the command line in this directory.

```bash
conda env create -f <file_name>.yaml
// conda env create -f env-ubuntu.yaml
```

If you are re-running after the version changes, please first update your `conda` environment through the `.yaml` file of the corresponding operating system in the `env` directory.

```bash
conda activate <your_old_conda>
conda env update --file <file_name>.yaml
// conda env update --file env-ubuntu.yaml
```

If the `pm2` tool is not installed, please install it first. If there is a problem during the installation process, please refer to [Official Documentation](https://pm2.keymetrics.io/).

```bash
npm install pm2 -g
```

### Debugging

`Flask` does not support hot loading when debugging, so the `watch` function of `pm2` is used, it will restart the `Flask` process after monitoring the file changes, these configurations have been written in `process.json` , basically does not need to be modified, the default service port is `5050`, you can modify the port in the `app.py` file, if you need to modify and the backend is also debugging, please modify the algorithm port of `Express` Settings (in line 19 of the `{platform root directory}/api-center/routes/edit.js` file: `var algorithm_port = 5050;`).

```bash
pm2 start process.json
```

View the running processes in pm2:

```bash
pm2 list
```

View the output of running the program in pm2:

```bash
pm2 log algrithm-center-exhibit
```

Other operations:

```bash
# Stop the specified process
pm2 stop algrithm-center-exhibit
# stop all processes
pm2 stop all
```

```bash
# Restart the specified process
pm2 restart algrithm-center-exhibit
# restart all processes
pm2 restart all
```

```bash
# delete the specified process
pm2 delete algrithm-center-exhibit
# delete all processes
pm2 delete all
```