new Vue({
    el: '#app',
    data: function() {
      return {
            activeIndex: '/edit',
            taskId: '',
            projectId: '',
            resultId: '',
            videoPath: ''
        }
    },
    methods: {
        handleSelect(key) {
            window.location.href = key;
        },
        rework() {
            window.location.href = `/edit/video-cloth-ads/editor/${this.taskId}/${this.projectId}`;
        },
        match() {
            window.location.href = '/edit/video-cloth-ads/match/' + this.taskId;
        },
        download() {
            let a = document.createElement('a');
            document.body.appendChild(a);
            a.href = this.videoPath;
            a.download = `video-${this.taskId}-${this.resultId}.mp4`;
            a.click();
            document.body.removeChild(a);
        }
    },
    mounted() {
        let temp = window.location.href.split('/');
        let resultId = temp[temp.length - 1];
        let projectId = temp[temp.length - 2];
        let taskId = temp[temp.length - 3];
        this.taskId = taskId;
        this.projectId = projectId;
        this.resultId = resultId;
        this.videoPath = `/tempoFiles/videos/${resultId}.mp4`;

    }
})