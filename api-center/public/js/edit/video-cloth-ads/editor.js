new Vue({
    el: '#app',
    data: function() {
      return {
            activeIndex: '/edit',
            taskId: '',
            projectId: '',
            loading: false,
            shotLine: [],
            candidates: [],
            choose: -1,
            candidateChoose: -1,
            saveLoading: false,
            sagLoading: false,
            previewAllVideo: null,
            previewLoading: false
        }
    },
    methods: {
        handleSelect(key) {
            window.location.href = key;
        },
        getProjectInfo() {
            let that = this;
            this.loading = true;
            axios.post('/edit/video-cloth-ads/get-project-info', {
                taskId: this.taskId,
                projectId: this.projectId
              })
            .then(function (res) {
              that.loading = false;
              let data = res.data;
              that.shotLine = data.shotLine;
              that.candidates = data.candidates;
            })
            .catch(function (error) {
              console.log(error);
            });
        },
        chooseShot(index, shot) {
            this.choose = index;
            for(let i = 0; i < this.candidates[index].length; i++) {
                if(this.candidates[index][i].id == shot.id) {
                    this.candidateChoose = i;
                    break;
                }
            }
            this.changeVideoSrc(shot.video);
        },
        chooseCandidate(index, shot) {
            this.candidateChoose = index;
            this.shotLine[this.choose] = shot;
            this.changeVideoSrc(shot.video);
            this.changeImageSrc(this.choose, shot.thumbnail);
        },
        changeVideoSrc(url) {
            let player = document.getElementById("preview-player");
            player.src = url;
        },
        changeImageSrc(index, url) {
            let img = document.getElementById("preview-image-" + index);
            img.src = url;
        },
        haveChoose(index) {
            return index == this.choose;
        },
        notChoose(index) {
            return this.choose != -1 && index != this.choose;
        },
        haveCandiChoose(index) {
            return index == this.candidateChoose;
        },
        notCandiChoose(index) {
            return this.candidateChoose != -1 && index != this.candidateChoose;
        },
        back() {
            window.location.href = '/edit/video-cloth-ads/match/' + this.taskId;
        },
        save() {
            let that = this;
            this.saveLoading = true;
            axios.post('/edit/video-cloth-ads/save-project-info', {
                taskId: this.taskId,
                projectId: this.projectId,
                projectInfo: {
                    shotLine: this.shotLine,
                    candidates: this.candidates
                }
              })
            .then(function (res) {
              that.saveLoading = false;
              that.$notify({
                title: '保存成功',
                message: '当前剪辑环境已保存',
                type: 'success',
                duration: 0
              });
            //   let data = res.data;
            })
            .catch(function (error) {
              console.log(error);
            });
        },
        saveAndGenerate() {
            let that = this;
            this.sagLoading = true;
            axios.post('/edit/video-cloth-ads/save-and-generate', {
                taskId: this.taskId,
                projectId: this.projectId,
                projectInfo: {
                    shotLine: this.shotLine,
                    candidates: this.candidates
                }
              })
            .then(function (res) {
              that.sagLoading = false;
              let data = res.data;
              let resultId = data.resultId;
              window.location.href = `/edit/video-cloth-ads/result/${that.taskId}/${that.projectId}/${resultId}`;
            })
            .catch(function (error) {
              console.log(error);
            });
        },
        previewAll() {
            let that = this;
            this.previewLoading = true;
            axios.post('/edit/video-cloth-ads/get-project-preview', {
                taskId: this.taskId,
                projectId: this.projectId,
                projectInfo: {
                    shotLine: this.shotLine,
                    candidates: this.candidates
                }
              })
            .then(function (res) {
              that.previewLoading = false;
              let data = res.data;
              let video = data.video;
              let player = document.getElementById("preview-all-player");
              player.src = video;
              that.previewAllVideo = video;
              that.$notify({
                title: '预览生成成功',
                message: '点击播放器播放即可开始预览，使用播放器右下角列表中的“画中画”模式体验更佳',
                type: 'success',
                duration: 0
              });
            })
            .catch(function (error) {
              console.log(error);
            });
        }
    },
    mounted() {
        let temp = window.location.href.split('/');
        let projectId = temp[temp.length - 1];
        let taskId = temp[temp.length - 2];
        this.taskId = taskId;
        this.projectId = projectId;
        this.getProjectInfo();
    }
})