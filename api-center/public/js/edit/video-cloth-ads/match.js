new Vue({
    el: '#app',
    data: function() {
      return {
            activeIndex: '/edit',
            taskId: '',
            matchResult: [],
            loading: false,
            editLoading: false
        }
    },
    methods: {
        handleSelect(key) {
            window.location.href = key;
        },
        getMatchResult() {
            let that = this;
            axios.post('/edit/video-cloth-ads/get-match-result', {
                taskId: this.taskId
              })
            .then(function (res) {
              let data = res.data;
              that.matchResult = data.match_result;
            })
            .catch(function (error) {
              console.log(error);
            });
        },
        generateVideo(template) {
            let that = this;
            this.loading = true;
            axios.post('/edit/video-cloth-ads/generate-video', {
                taskId: this.taskId,
                template: template
            })
            .then(function (res) {
                let data = res.data;
                let resultId = data.resultId;
                // 跳转到结果页面
                window.location.href = `/edit/video-cloth-ads/result/${that.taskId}/default/${resultId}`;
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        customModifi(template) {
            this.editLoading = true;
            let that = this;
            axios.post('/edit/video-cloth-ads/create-project', {
                taskId: this.taskId,
                template: template
            })
            .then(function (res) {
                that.editLoading = false;
                let data = res.data;
                let projectId = data.projectId;
                // 跳转到结果页面
                window.location.href = `/edit/video-cloth-ads/editor/${that.taskId}/${projectId}`;
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    },
    mounted() {
        let temp = window.location.href.split('/');
        let taskId = temp[temp.length - 1];
        this.taskId = taskId;
        this.getMatchResult();
    }
})