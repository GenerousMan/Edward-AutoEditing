new Vue({
    el: '#app',
    data: function() {
      return {
            activeIndex: '/edit',
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
        handleSelect(key) {
            window.location.href = key;
        },
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
          })
          .catch(function (error) {
            console.log(error);
          });
        },
        standBy() {
          this.$confirm('暂时离开后，可以在XXX中查看任务进度，以及返回到该任务的页面', '提示', {
              confirmButtonText: '确定',
              cancelButtonText: '取消'
            }).then(() => {
              window.location.href = '/edit';
            }).catch(() => {
              
            });
        },
        cancelTask() {
          this.$confirm('任务取消后，素材预处理的数据将会被清除', '警告', {
              confirmButtonText: '确定取消',
              cancelButtonText: '不取消',
              type: 'warning'
            }).then(() => {

            }).catch(() => {
              
            });
        },
        isFinished() {
          return this.trans == 100 && this.yolo == 100 && this.alphapose == 100 &&
            this.features == 100 && this.match == 100 && this.render == 100;
        },
        jump(key) {
          if(key == 'match') {
            window.location.href = '/edit/video-cloth-ads/match/' + this.taskId;
          } else if (key == 'out') {

          } else {

          }
          
        }
    },
    mounted() {
        let temp = window.location.href.split('/');
        let taskId = temp[temp.length - 1];
        this.taskId = taskId;
        // 首先进行一次更新
        this.getTaskProgress();
        // 然后启动定时查询任务, 2s一次
        let that = this;
        this.interval = setInterval(() => {
            that.getTaskProgress();
            if (that.isFinished()) {
              clearInterval(that.interval);
              that.$notify({
                title: '预处理完毕',
                message: '点击“查看匹配结果”按钮跳转到浏览页面',
                type: 'success',
                duration: 0
              });
            }
        }, 2000);
    }
})