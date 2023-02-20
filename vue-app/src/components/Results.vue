<template>
    <div class="background">
        <div class="center-box">
            <div class="title-box">
                <div class="title">
                    剪辑结果
                </div>
                <div class="intro">
                    以下就是系统针对素材的推荐剪辑结果
                </div>
                <div class="back">
                    STEP-4
                </div>
                <div class="btn-box">
                    <div class="btn" @click="home()">
                        <div class="border"></div>
                        <img src="@/assets/home.jpg"/>
                        回到主页
                    </div>
                    <div class="btn" @click="again()">
                        <div class="border"></div>
                        <img src="@/assets/again.jpg"/>
                        再试一次
                    </div>
                </div>
            </div>
            <!-- <div class="results-box"> -->
            <transition-group name="fade" tag="div" class="results-box">
                <div class="card" v-for="(video, index) in videos" :key="video.template_video">
                    <div class="video">
                        <video :class="{ canplay: getStatus(index), playing: playing[index] }" @canplay="setStatus(index)" @play="play(index)" @pause="pause(index)" controls="controls">
                            <source :src="video.result_video" type="video/mp4">
                        </video>
                    </div>
                </div>
            </transition-group>
            <!-- </div> -->
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Wait',
    data: () => {
        return {
            taskId: '',
            videos: [],
            canplay: [],
            playing: [],
            path: ''
        }
    },
    methods: {
        initStatus(videos) {
            for(let i = 0; i < videos.length; i++) {
                this.canplay.push(false);
                this.playing.push(false);
            }
        },
        setStatus(index) {
            this.$set(this.canplay, index, true);
        },
        getStatus(index) {
            return this.canplay[index];
        },
        play(index) {
            this.$set(this.playing, index, true);
            this.refresh();
        },
        pause(index) {
            this.$set(this.playing, index, false);
            this.refresh();
        },
        home() {
            this.$router.push({ path: '/exhibit' });
        },
        again() {
            this.$router.push({ path: '/exhibit/select' });
        },
        homev2(path) {
            if(this.$route.path != '/exhibit' && this.$route.path == path) {
                this.$router.push({ path: '/exhibit' });
            }
        },
        refresh() {
            clearTimeout(this.timeout);
            let that = this;
            // 五分钟内没有操作 自动回到首页
            this.timeout = setTimeout(function(){
                that.homev2(that.path);
            }, 5 * 60 * 1000);
        },
        scroll() {
            // this.refresh();
        }
    },
    mounted() {
        let that = this;
        this.taskId = this.$route.params.taskId;
        this.$emit("loading", '获取数据中');
        axios.post('/edit/exhibit/get-results', {
            taskId: this.taskId
        }).then(response => {
            let videos = response.data.results;
            that.initStatus(videos);
            that.videos = videos;
            this.$emit("cancelLoading");
        }).catch(function (error) { // 请求失败处理
            console.log(error);
            this.$emit("cancelLoading");
        });
        // this.refresh();
        this.path = this.$route.path;
        // let app = document.getElementById('app');
        // app.addEventListener("scroll", this.scroll);
    },
    beforeDestroy() {
        // clearTimeout(this.timeout);
        // let app = document.getElementById('app');
        // app.removeEventListener("scroll", this.scroll);
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
    /* background: rgba(255, 255, 255, 0.5); */
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

.results-box {
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

.video {
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: 0;
}

.video video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(70%) blur(0px);
    transform: scale;
    opacity: 0;
    transition: all 300ms;
}

.card:hover .video video {
    filter: brightness(100%) blur(0px);
}

.canplay {
    opacity: 1 !important;
}

.playing {
    filter: brightness(100%) !important;
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
    top: 9px;
    left: 40px;
    width: 32px;
    height: 32px;
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
</style>