<template>
    <div class="background">
        <div class="center-box">
            <div class="title-box">
                <div class="title">
                    选择视频
                </div>
                <div class="intro">
                    在素材提供的视频中，选择想要使用的视频，时长至少需要60s
                </div>
                <div class="back">
                    STEP-2
                </div>
                <div class="back-btn" @click="back()">
                    <img src="@/assets/left-back.svg"/>
                </div>
            </div>
            <transition-group name="fade" tag="div" class="card-box">
            <!-- <div class="card-box"> -->
                <!-- <transition-group name="fade"> -->
                    <div :class="['card', { selected: getSelectedIndex(video) != -1 }]" v-for="(video, index) in videos" :key="video.name" @click="add(video)">
                        <div class="back-video">
                            <video :class="{ canplay: getStatus(index) }" loop="loop" autoplay="autoplay" muted @canplay="setStatus(index)">
                                <source :src="video.url" type="video/mp4">
                            </video>
                        </div>
                        <div class="duration">
                            {{video.dura}}s
                        </div>
                        <div class="cancel" @click.stop="remove(video)">
                            <img src="@/assets/cancel-2.png"/>
                        </div>
                    </div>
                <!-- </transition-group> -->
                <div class="card hidden" v-if="videos.length % 3 != 0" key="hidden"></div>
            <!-- </div> -->
            </transition-group>
        </div>
        <div class="select-box">
            <div :class="['select', {'select-empty': selected.length == 0}]">
                <div class="btns">
                    <div class="btn random" @click="random()">
                        随机选择
                    </div>
                    <div class="btn all" @click="all()">
                        全部选择
                    </div>
                    <div class="btn all" @click="clear()">
                        清空已选
                    </div>
                    <div class="btn dura" @click="clear()" v-if="limit - getDuration() > 0">
                        还需要选择 {{limit - getDuration()}} s
                    </div>
                    <div class="btn dura enough" @click="clear()" v-else>
                        已选择 {{getDuration()}} s
                    </div>
                    <div class="btn begin" @click="begin()">
                        开始剪辑
                    </div>
                </div>
                <div class="scroll-box" id="scroll-box">
                    <div class="select-cards">
                        <div class="card" v-for="video in selected" :key="video.name">
                            <div class="back-video">
                                <video loop="loop" autoplay="autoplay" muted>
                                    <source :src="video.url" type="video/mp4">
                                </video>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Videos',
    data: () => {
        return {
            name: '',
            videos: [],
            selected: [],
            canplay: [],
            limit: 60,
            path: ''
        }
    },
    mounted() {
        let that = this;
        this.name = this.$route.params.name;
        // load videos of this name
        this.$emit("loading", '获取视频数据中');
        axios.post('/edit/exhibit/get-videos', {
            name: this.name
        }).then(response => {
            // console.log(response);
            let videos = response.data.videos;
            that.initStatus(videos);
            that.videos = videos;
            console.log(that.videos);
            this.$emit("cancelLoading");
        }).catch(function (error) { // 请求失败处理
            console.log(error);
            this.$emit("cancelLoading");
        });
        this.refresh();
        this.path = this.$route.path;
        let app = document.getElementById('app');
        app.addEventListener("scroll", this.scroll);
    },
    beforeDestroy() {
        clearTimeout(this.timeout);
        let app = document.getElementById('app');
        app.removeEventListener("scroll", this.scroll);
    },
    methods: {
        add(video) {
            if(this.getSelectedIndex(video) == -1) {
                this.selected.push(video);
            }
            this.refresh();
        },
        remove(video) {
            // console.log(this.getSelectedIndex(video));
            // console.log(this.selected);
            if(this.getSelectedIndex(video) != -1) {
                this.selected.splice(this.getSelectedIndex(video), 1);
            }
            // console.log(this.selected);
            this.refresh();
        },
        random() {
            while(this.getDuration() < this.limit) {
                let index = Math.floor(Math.random() * Math.floor(this.videos.length));
                let video = this.videos[index];
                if(this.getSelectedIndex(video) == -1) {
                    this.selected.push(video);
                }
            }
            this.refresh();
        },
        all() {
            this.selected = Array.from(this.videos);
            this.refresh();
        },
        clear() {
            this.selected = [];
            this.refresh();
        },
        begin() {
            let that = this;
            this.refresh();
            if(this.getDuration() >= this.limit) {
                this.$emit("loading", '创建任务中');
                axios.post('/edit/exhibit/select-begin', {
                    name: this.name,
                    videos: this.videos,
                    selected: this.selected
                }).then(response => {
                    // console.log(response);
                    let taskId = response.data.taskId;
                    this.$emit("cancelLoading");
                    that.$router.push({ path: `/exhibit/wait/${taskId}` });
                }).catch(function (error) { // 请求失败处理
                    console.log(error);
                    this.$emit("cancelLoading");
                });
            }
        },
        getSelectedIndex(video) {
            let index = -1;
            for(let i = 0; i < this.selected.length; i++) {
                if(this.selected[i].name == video.name) {
                    index = i;
                    break;
                }
            }
            return index;
        },
        getDuration() {
            let duration = 0;
            for(let i = 0; i < this.selected.length; i++) {
                duration += this.selected[i].dura;
            }
            return duration;
        },
        initStatus(videos) {
            for(let i = 0; i < videos.length; i++) {
                this.canplay.push(false);
            }
        },
        setStatus(index) {
            this.$set(this.canplay, index, true)
        },
        getStatus(index) {
            return this.canplay[index];
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
            this.refresh();
        },
        back() {
            this.$router.push({ path: '/exhibit/select' });
        }
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

.back-img, .back-video {
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: 0;
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

.back-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(60%) blur(0px);
    transform: scale(1.02);
    transition: all 300ms;
}

.back-video video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(70%) blur(0px);
    transform: scale(1.02);
    opacity: 0;
    transition: all 300ms;
}

.cancel {
    position: absolute;
    top: 16px;
    right: 16px;
    /* width: 64px;
    height: 64px; */
    padding: 12px 24px;
    text-align: center;
    border-radius: 8px 8px;
    background: rgba(168, 0, 0, 0.6);
    backdrop-filter: blur(10px);
    opacity: 0;
    transition: all 300ms;
}

.cancel img {
    position: relative;
    top: 2px;
    width: 32px;
    height: 32px;
}

.card:hover .back-video video {
    filter: brightness(100%) blur(0px);
}

.card:hover .back-img img {
    filter: brightness(100%) blur(0px);
}

.selected .back-video video {
    filter: brightness(100%) blur(0px);
}

.selected .cancel {
    opacity: 1;
}

.canplay {
    opacity: 1 !important;
}

.select-box {
    position: fixed;
    bottom: 0px;
    left: 0px;
    width: 100%;
    height: 240px;
    z-index: 99;
    /* background: white; */
}

.select {
    position: relative;
    top: 0px;
    margin: 0 auto;
    width: 70%;
    height: 100%;
    border-radius: 8px 8px 0 0;
    background: rgba(173, 173, 173, 0.5);
    backdrop-filter: blur(10px);
    /* overflow-x: scroll; */
    transition: all 300ms;
}

.select-empty {
    top: 170px;
}

.scroll-box {
    /* height: 100%; */
    width: 100%;
    overflow-x: scroll;
}

.select-cards {
    display: flex;
    width: max-content;
    padding: 16px;
    height: 160px;
    box-sizing: border-box;
}

.select-cards .card {
    margin-right: 8px;
    margin-left: 8px;
    width: 160px;
    height: 100%;
    user-select: none;
}

.select-cards .card .back-video video{
    opacity: 1;
}

.btns {
    display: flex;
    height: 60px;
    margin-left: 16px;
}

.btn {
    position: relative;
    margin: 12px 8px;
    width: max-content;
    height: max-content;
    padding: 4px 34px 6px 34px;
    text-align: center;
    line-height:36px;
    background: rgb(27, 27, 27);
    color: white;
    font-weight: bold;
    font-size: 18px;
    cursor: pointer;
    border-radius: 8px;
}

.begin {
    position: absolute;
    right: 16px;
    color: rgb(27, 27, 27);
    background: rgb(255, 179, 0);
}

.dura {
    position: absolute;
    right: 178px;
    /* color: rgb(27, 27, 27); */
    color: white;
    background: #F56C6C;
}

.hidden {
    cursor: default;
    opacity: 0;
}

.enough {
    color: white;
    background: #67C23A;
}
</style>

<style>
#scroll-box::-webkit-scrollbar{
    /* display: none; */
    width: 12px;
    height: 12px;
    background-color: transparent !important;
    /* background-color: #ccc; */
    /* background-color: rgb(27, 27, 27); */
}
/*滚动条的上下两端的按钮*/
#scroll-box::-webkit-scrollbar-button{
    height: 0px;
    width: 24px;
    /* background-color: #333; */
}
</style>

