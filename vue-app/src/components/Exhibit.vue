<template>
    <div>
        <!-- This is {{ msg }} -->
        <div class="box">
            <div class="title">
                飞 影 · Cut Minutes
            </div>
            <div class="sub-title">
                智能剪辑电商展示短视频
            </div>
            <div class="intro">
                上传视频素材，AI智能挑选完美的镜头组合<br>
                一键点击，分秒完成
            </div>
            <div class="btn" @click="begin()">
                <div class="border"></div>
                <img src="@/assets/begin.jpg"/>
                开始剪辑
            </div>
        </div>
        <div class="background">
            <!-- <img src="@/assets/back_left.jpg"/> -->
            <video :class="{ canplay: canplay }" loop="loop" autoplay="autoplay" muted @canplay="canplay = true">
                <source src="@/assets/home-back.mp4" type="video/mp4">
            </video>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Exhibit',
    data: () => {
        return {
            canplay: false
        }
    },
    methods: {
        begin() {
            this.$router.push({ path: '/exhibit/select' })
        }
    }
}
</script>

<style scoped>
.box {
    position: absolute;
    top: 30%;
    left: 20%;
    z-index: 1;
    color: white;
    user-select: none;
}

.title {
    font-size: 72px;
    font-weight: bold;
    margin-bottom: 8px;
}

.sub-title {
    font-size: 52px;
    font-weight: 100;
    margin-bottom: 24px;
}

.intro {
    font-size: 24px;
    font-weight: 100;
    line-height: 48px;
    margin-bottom: 36px;
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

.background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: 0;
    user-select: none;
}

.background img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(50%) blur(0px);
    transform: scale(1.02);
}

.background video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0;
    filter: brightness(50%) blur(5px);
    transform: scale(1.02);
    transition: all 300ms;
}

.canplay {
    opacity: 1 !important;
}

</style>

