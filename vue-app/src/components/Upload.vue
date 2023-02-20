<template>
    <div class="background">
        <div class="center-box">
            <div class="title-box">
                <div class="title">
                    上传视频
                </div>
                <div class="intro">
                    点击下方的按钮选择或者拖拽视频到按钮区域内，然后开始上传
                </div>
                <div class="back">
                    STEP-2
                </div>
                <div class="btn-box">
                    <div class="btn" @click="upload()">
                        <div class="border"></div>
                        <img src="@/assets/upload-rocket.png"/>
                        上传素材
                    </div>
                    <div class="btn" @click="clear()">
                        <div class="border"></div>
                        <img src="@/assets/upload-clear.png"/>
                        重新选择
                    </div>
                </div>
                <div class="back-btn" @click="back()">
                    <img src="@/assets/left-back.svg"/>
                </div>
            </div>
            <!-- <div class="card-box"> -->
            <transition-group name="fade" tag="div" class="card-box">
                <div class="card block" key="choose">
                    <div class="upload-box"
                        @click="chooseFile">
                        <transition name="fade">
                            <div class="upload-tip" v-if="!drag">
                                <div class="icon">
                                    <img src="@/assets/file-add-line.png"/>
                                </div>
                                <div class="info">
                                    点击选择 或 拖拽视频到框内
                                </div>
                            </div>
                            <div class="drop-tip" v-else>
                                <div class="icon">
                                    <img src="@/assets/mouse-line.png"/>
                                </div>
                                <div class="info">
                                    已拖拽到框内 松开鼠标即可
                                </div>
                            </div>
                        </transition>
                        <div class="drag-mask"
                            @dragenter.stop.prevent="dragIn"
                            @dragleave.stop.prevent="dragOut"
                            @dragover.stop.prevent
                            @drop.stop.prevent="dropFiles"></div>
                    </div>
                </div>
                <div class="card" v-for="video in videos" :key="video.name">
                    <div class="back-video">
                        <video loop="loop" autoplay="autoplay" muted @loadedmetadata="loadedmetadata(video, $event)">
                            <source :src="video.src" :type="video.type">
                        </video>
                    </div>
                    <div class="duration">
                        <div :class="['bar', {finish: video.upload == 100}]" :style="{width: video.upload + '%'}"></div>
                        <div class="text">{{video.dura}}s</div>
                    </div>
                </div>
                <div class="card hidden" v-if="(videos.length + 1) % 3 != 0" key="hidden"></div>
            </transition-group>
            <!-- </div> -->
        </div>
        <input type="file" id="input" v-on:change="filesChange" multiple accept="video/*"/>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Upload',
    data: () => {
        return {
            drag: false,
            videos: [],
            files: [],
            checks: [],
            filenames: [],
            filter: '',
            path: ''
        }
    },
    methods: {
        chooseFile() {
            let input = document.getElementById('input');
            input.click();
            // this.refresh();
        },
        dragIn() {
            this.drag = true;
            window.console.log('drag-in');
        },
        dragOut() {
            this.drag = false;
            window.console.log('drag-out');
        },
        dropFiles(e) {
            this.drag = false;
            let dt = e.dataTransfer;
            this.loadFiles(dt.files);
            // this.refresh();
        },
        loadFiles(files) {
            for(let i = 0; i < files.length; i++) {
                let index = files[i].name.lastIndexOf(".");
                let ext = files[i].name.substr(index+1).toLowerCase();
                let allows = ['mp4', 'flv', 'avi', 'mkv', 'wmv', 'rmvb']
                if(allows.indexOf(ext) != -1) {
                    let name = files[i].name;
                    let last = files[i].lastModified;
                    let size = files[i].size;
                    let check = {name, last, size};
                    if(this.getCheckIndex(check) == -1) {
                        this.files.push(files[i]);
                        this.checks.push(check);
                        let name = files[i].name;
                        let url = URL.createObjectURL(files[i]);
                        let type = files[i].type;
                        this.videos.push({ name: name, type: type, src: url, dura: 0, upload: 0});
                    } else {
                        alert('文件被重复选择: ' + files[i].name);
                    }
                } else {
                    alert('不支持的文件格式: ' + files[i].name);
                }
            }
        },
        getCheckIndex(check) {
            let index = -1;
            for(let i = 0; i < this.checks.length; i++) {
                let temp = this.checks[i];
                if(check.name == temp.name && check.last == temp.last && check.size == temp.size) {
                    index = i;
                    break;
                }
            }
            return index;
        },
        filesChange() {
            let input = document.getElementById('input');
            // this.loadFile(input.files[0]);
            this.loadFiles(input.files);
        },
        loadedmetadata(video, event) {
            let duration = parseInt(event.target.duration);
            video.dura = duration;
        },
        async upload() {
            this.$emit("loading", '上传视频中');
            for(let i = 0; i < this.videos.length; i++) {
                let video = this.videos[i];
                let file = this.files[i];
                if(video.upload != 100) {
                    await this.uploadVideo(file, video);
                    // this.refresh();
                }
            }
            let allSuccess = true;
            let failVideos = [];
            for(let i = 0; i < this.videos.length; i++) {
                let video = this.videos[i];
                if(video.upload != 100) {
                    allSuccess = false;
                    failVideos.push(video);
                }
            }
            if(allSuccess) {
                // this.allSuccess = allSuccess;
                // this.$notify({
                //     title: '上传成功',
                //     message: '所有视频已经上传完毕',
                //     type: 'success',
                //     duration: 0
                //   });
                this.beginProcess();
                this.$emit("cancelLoading");
            } else {
                console.log(failVideos);
                alert('部分视频上传失败，请尝试再次点击上传');
                // this.$notify.error({
                //     title: '错误',
                //     message: failVideos.length+'个视频上传失败，请尝试再次上传',
                //     duration: 0
                // });
                this.$emit("cancelLoading");
            }
        },
        clear() {
            this.videos = [];
            this.files = [];
            this.checks = [];
            // this.refresh();
        },
        uploadVideo(file, video) {
            let param = new FormData();
            param.append('file', file);
            return axios({
                url: '/edit/upload',
                method: 'post',
                headers: {
                    'Content-Type':'multipart/form-data'
                },
                data: param,
                onUploadProgress: function(event) {
                    if(event.lengthComputable) {
                        let percent = parseInt(Math.floor(event.loaded / event.total * 100));
                        video.upload = percent;
                    }
                },
            })
            .then(res => {
                let data = res.data;
                this.filenames.push(data.filename);
            })
            .catch(error => {
                window.console.log(error);
                video.status = 'exception';
            });
        },
        beginProcess() {
            let that = this;
            this.$emit("loading", '创建任务中');
            axios.post('/edit/exhibit/upload-begin',{
                filenames: this.filenames,
                filter: this.filter
            })
            .then(res => {
                that.loading = false;
                let data = res.data;
                let taskId = data.taskId;
                // window.location.href = `/edit/video-cloth-ads/preprocess/${taskId}`
                this.$emit("cancelLoading");
                that.$router.push({ path: `/exhibit/wait/${taskId}` });
            })
            .catch(e => {
                window.console.log(e);
                this.$emit("cancelLoading");
            });
        },
        home(path) {
            if(this.$route.path != '/exhibit' && this.$route.path == path) {
                this.$router.push({ path: '/exhibit' });
            }
        },
        refresh() {
            clearTimeout(this.timeout);
            let that = this;
            // 五分钟内没有操作 自动回到首页
            this.timeout = setTimeout(function(){
                that.home(that.path);
            }, 5 * 60 * 1000);
        },
        scroll() {
            // this.refresh();
        },
        back() {
            this.$router.push({ path: '/exhibit/select' });
        }
    },
    mounted() {
        // this.refresh();
        this.path = this.$route.path;
        // let app = document.getElementById('app');
        // app.addEventListener("scroll", this.scroll);
    },
    beforeDestroy() {
        clearTimeout(this.timeout);
        let app = document.getElementById('app');
        app.removeEventListener("scroll", this.scroll);
    }
}
</script>

<style scoped>
.background {
    width: 100%;
    min-height: 100%;
    height: max-content;
    background: rgb(27, 27, 27);
}

.center-box {
    width: 80%;
    margin: 0 auto;
}

.title-box {
    position: relative;
    padding-top: 150px;
    color: white;
    user-select: none;
}

.title {
    font-size: 48px;
    font-weight: bold;
    margin-bottom: 12px;
    z-index: 2;
}

.intro {
    font-size: 24px;
    font-weight: 100;
    z-index: 2;
}

.back {
    position: absolute;
    top: 64px;
    left: 24px;
    font-weight: bold;
    font-size: 200px;
    z-index: 1;
    opacity: 0.2;
}

.back-btn {
    position: absolute;
    top: 24px;
    width: 120px;
    height: 60px;
    text-align: center;
    cursor: pointer;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.1);
    z-index: 10;
    transition: all 300ms;
}

.back-btn:hover {
    background: rgba(255, 255, 255, 0.2);
}

.back-btn img {
    position: relative;
    top: 6px;
    /* left: -12px; */
    height: 48px;
    /* fill: white; */
    /* filter: drop-shadow(#ffffff 80px 0); */
}

.card-box {
    margin-top: 120px;
    padding-bottom: 240px;
    /* height: 200px; */
    height: max-content;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
}

.card {
    position: relative;
    margin-bottom: 64px;
    width: 30%;
    height: 400px;
    border-radius: 8px;
    background: rgba(173, 173, 173, 0.5);
    overflow: hidden;
    cursor: pointer;
}

.block {
    display: flex;
    /* width: 1136px;
    height: 600px; */
}

.upload-box {
    position: relative;
    margin: 0 auto;
    width: 100%;
    height: 100%;
}

.upload-box:hover .upload-tip{
    background-color: rgb(231, 231, 231);
    border-color: transparent;
}

.icon {
    margin: 0 auto;
    margin-top: 35%;
    width: 48px;
    height: 48px;
}

.icon img {
    width: 48px;
    opacity: 0.8;
}

.info {
    margin:0 auto;
    margin-top: 6px;
    width: max-content;
    color: rgb(151, 151, 151);
}

#input {
    display: none;
}

.drag-mask {
    position: absolute;
    top: 0px;
    width: 100%;
    height: 100%;
    cursor: pointer;
}
.upload-tip {
    position: absolute;
    top: -2px;
    left: -2px;
    width: 100%;
    height: 100%;
    /* border: dashed 2px rgb(200, 200, 200); */
    border-radius: 8px;
    cursor: pointer;
    transition: all 300ms;
}
.drop-tip {
    position: absolute;
    top: -2px;
    left: -2px;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    /* border: solid 2px transparent; */
    border-radius: 8px;
    cursor: pointer;
    transition: all 300ms;
}

.back-video {
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: 0;
}

.back-video video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(90%) blur(0px);
    transform: scale(1.02);
    opacity: 1;
    transition: all 300ms;
}

.duration {
    position: absolute;
    bottom: 16px;
    right: 16px;
    padding: 0 12px;
    font-size: 64px;
    font-weight: bold;
    color: white;
    z-index: 1;
    border-radius: 8px 8px;
    background: rgba(173, 173, 173, 0.5);
    backdrop-filter: blur(10px);
}

.duration .bar {
    position: absolute;
    top: 0px;
    left: 0px;
    width: 20%;
    height: 100%;
    border-radius: 8px 8px;
    background: #409EFF;
    backdrop-filter: blur(10px);
    z-index: 3;
}

.duration .finish {
    background: #67C23A;
}

.duration .text {
    position: relative;
    z-index: 4;
}

.btn-box {
    position: absolute;
    top: 140px;
    right: 0px;
}

.btn {
    position: relative;
    top: 0px;
    left: 0px;
    color: black;
    font-weight: bold;
    font-size: 20px;
    padding: 12px 48px 12px 80px;
    border-radius: 8px;
    width: max-content;
    background: rgba(255, 255, 255, 1);
    cursor: pointer;
    margin-bottom: 32px;
    transition: all 100ms;
}

.btn img {
    position: absolute;
    top: 12px;
    left: 40px;
    width: 28px;
    height: 28px;
}

.btn .border {
    position: absolute;
    top: 6px;
    left: 6px;
    width: 98%;
    height: 93%;
    border-radius: 8px;
    border: 3px solid white;
    transition: all 100ms;
}

.btn:hover {
    top: -2px;
    left: -2px;
}

.btn:hover .border {
    top: 10px;
    left: 10px;
}

.hidden {
    cursor: default;
    opacity: 0;
}
</style>

