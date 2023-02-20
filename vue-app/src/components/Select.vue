<template>
    <div class="background">
        <div class="center-box">
            <div class="title-box">
                <div class="title">
                    选择素材
                </div>
                <div class="intro">
                    请选择一套视频作为素材，也可以上传自己拍摄的素材
                </div>
                <div class="back">
                    STEP-1
                </div>
            </div>
            <div class="card-box">
                <div class="card" @click="jump('senma-1')">
                    <div class="back-video">
                        <video :class="{ canplay: canplay[0] }" loop="loop" autoplay="autoplay" muted @canplay="setcanplay(0)">
                            <source src="@/assets/senma-1-mix-reduce.mp4" type="video/mp4">
                        </video>
                    </div>
                    <div class="content">
                        <div class="btn">
                            <div class="border"></div>
                            选择素材
                        </div>
                    </div>
                </div>
                <div class="card" @click="jump('senma-2')">
                    <div class="back-video">
                        <video :class="{ canplay: canplay[1] }" loop="loop" autoplay="autoplay" muted @canplay="setcanplay(1)">
                            <source src="@/assets/senma-2-mix-reduce.mp4" type="video/mp4">
                        </video>
                    </div>
                    <div class="content">
                        <div class="btn">
                            <div class="border"></div>
                            选择素材
                        </div>
                    </div>
                </div>
                <div class="card" @click="jump('white-girl')">
                    <div class="back-video">
                        <video :class="{ canplay: canplay[2] }" loop="loop" autoplay="autoplay" muted @canplay="setcanplay(2)">
                            <source src="@/assets/white-girl-mix-reduce.mp4" type="video/mp4">
                        </video>
                    </div>
                    <div class="content">
                        <div class="btn">
                            <div class="border"></div>
                            选择素材
                        </div>
                    </div>
                </div>
                <div class="card" @click="jump('blue-boy')">
                    <div class="back-video">
                        <video :class="{ canplay: canplay[3] }" loop="loop" autoplay="autoplay" muted @canplay="setcanplay(3)">
                            <source src="@/assets/blue-boy-mix-reduce.mp4" type="video/mp4">
                        </video>
                    </div>
                    <div class="content">
                        <div class="btn">
                            <div class="border"></div>
                            选择素材
                        </div>
                    </div>
                </div>
                <div class="card upload-card" @click="jump('upload')">
                    <div class="back-img">
                        <img src="@/assets/upload-back.jpg"/>
                    </div>
                    <div class="content">
                        <div class="btn">
                            <div class="border"></div>
                            上传素材
                        </div>
                    </div>
                    <div class="icon-box">
                        <img class="icon" src="@/assets/upload.png"/>
                    </div>
                </div>
                <div class="card hidden"></div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Select',
    data: () => {
        return {
            timeout: null,
            canplay: [false, false, false, false],
            path: ''
        }
    },
    methods: {
        jump(name) {
            this.$router.push({ path: `/exhibit/select/${name}` });
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
        setcanplay(index) {
            this.$set(this.canplay, index, true);
        }
    },
    mounted() {
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

.card-box {
    margin-top: 120px;
    padding-bottom: 150px;
    /* height: 200px; */
    height: max-content;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    user-select: none;
}

.card {
    position: relative;
    margin-bottom: 64px;
    width: 48%;
    height: 400px;
    border-radius: 8px;
    background: rgba(173, 173, 173, 0.5);
    overflow: hidden;
}

.content {
    position: absolute;
    left: 50%;
    margin-left: -90px;
    bottom: 30px;
    /* padding-left: 24px; */
    z-index: 2;
}

.card-title {
    font-size: 36px;
    font-weight: bold;
    margin-bottom: 12px;
    z-index: 2;
    color: white;
}

.back-img {
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: 0;
}

.back-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(50%) blur(0px);
    transform: scale(1.02);
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
    filter: brightness(50%) blur(0px);
    transform: scale(1.02);
    opacity: 0;
    transition: all 300ms;
}

.canplay {
    opacity: 1 !important;
}

.btn {
    position: relative;
    top: 0px;
    left: 0px;
    color: rgb(27, 27, 27);
    font-weight: bold;
    font-size: 20px;
    padding: 12px 48px 12px 48px;
    border-radius: 8px;
    width: max-content;
    height: max-content;
    background: rgba(255, 255, 255, 1);
    cursor: pointer;
    /* align-self: flex-end; */
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

.upload-card {
    background: rgba(255, 255, 255, 0.5);
    text-align: center;
}

.upload-card .icon {
    margin-top: 120px;
    width: 120px;
}

.icon-box {
    position: absolute;
    width: 100%;
    height: 100%;
}

.hidden {
    cursor: default;
    opacity: 0;
}
</style>

