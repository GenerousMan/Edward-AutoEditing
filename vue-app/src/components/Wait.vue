<template>
    <div class="background">
        <div class="center-box">
            <div class="title-box">
                <div class="title">
                    等待结果
                </div>
                <div class="intro">
                    等待系统匹配计算以及生成视频
                </div>
                <div class="back">
                    STEP-3
                </div>
            </div>
            <div class="progress-box">
                <div class="all progress">
                    <div class="name">整体进度</div>
                    <div :class="['bar', {finish: all() == 100}]" :style="{width:all()+'%'}"></div>
                </div>
                <div class="trans progress">
                    <div class="name">转码压缩</div>
                    <div :class="['bar', {finish: trans == 100}]" :style="{width:trans+'%'}"></div>
                </div>
                <div class="yolo progress">
                    <div class="name">人物识别</div>
                    <div :class="['bar', {finish: yolo == 100}]" :style="{width:yolo+'%'}"></div>
                </div>
                <div class="alphapose progress">
                    <div class="name">关节点提取</div>
                    <div :class="['bar', {finish: alphapose == 100}]" :style="{width:alphapose+'%'}"></div>
                </div>
                <div class="features progress">
                    <div class="name">镜头语义</div>
                    <div :class="['bar', {finish: features == 100}]" :style="{width:features+'%'}"></div>
                </div>
                <div class="match progress">
                    <div class="name">案例匹配</div>
                    <div :class="['bar', {finish: match == 100}]" :style="{width:match+'%'}"></div>
                </div>
                <div class="render progress">
                    <div class="name">剪辑生成</div>
                    <div :class="['bar', {finish: render == 100}]" :style="{width:render+'%'}"></div>
                </div>
            </div>
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
            interval: null,
            trans: 0,
            yolo: 0,
            alphapose: 0,
            features: 0,
            match: 0,
            render: 0
        }
    },
    methods: {
        getTaskProgress() {
          let that = this;
          axios.post('/edit/video-cloth-ads/get-task-progress', {
              taskId: this.taskId
            })
          .then(function (res) {
            let data = res.data;
            that.trans = data.trans;
            that.yolo = data.yolo;
            that.alphapose = data.alphapose;
            that.features = data.features;
            that.match = data.match;
            that.render = data.render;
            // that.all = that.getAll();
          })
          .catch(function (error) {
            console.log(error);
          });
        },
        isFinished() {
          return this.trans == 100 && this.yolo == 100 && this.alphapose == 100 &&
            this.features == 100 && this.match == 100 && this.render == 100;
        },
        all() {
            return (this.trans + this.yolo + this.alphapose + this.features + this.match + this.render) / 6;
        }
    },
    mounted() {
        let temp = window.location.href.split('/');
        let taskId = temp[temp.length - 1];
        this.taskId = taskId;
        // 首先进行一次更新
        this.getTaskProgress();
        // 然后启动定时查询任务, 1s一次
        let that = this;
        this.interval = setInterval(() => {
            that.getTaskProgress();
            if (that.isFinished()) {
              clearInterval(that.interval);
              that.$router.push({ path: `/exhibit/results/${that.taskId}` });
            }
        }, 2000);
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

.progress-box {
    margin-top: 120px;
    padding-bottom: 120px;
    height: max-content;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    user-select: none;
}

.progress {
    position: relative;
    margin-bottom: 32px;
    width: 49%;
    height: 100px;
    border-radius: 8px;
    background: rgb(56, 56, 56);
    overflow: hidden;
}

.all {
    width: 100%;
    margin-bottom: 64px;
}

.progress .name {
    position: relative;
    margin-left: 36px;
    font-size: 36px;
    font-weight: bold;
    color: rgb(255, 255, 255);
    line-height: 100px;
    z-index: 3;
}

.progress .bar {
    position: absolute;
    top: 0px;
    left: 0px;
    width: 30%;
    height: 100%;
    border-radius: 8px;
    background: #409EFF;
    transition: all 300ms;
}

.finish {
    background: #67C23A !important;
}

</style>