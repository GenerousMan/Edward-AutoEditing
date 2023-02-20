new Vue({
    el: '#app',
    data: function() {
      return {
            activeIndex: '/edit',
            filter: '',
            videos: [],
            filenames: [],
            allSuccess: false,
            loading: false
        }
    },
    methods: {
        handleSelect(key) {
            window.location.href = key;
        },
        chooseFile() {
            let input = document.getElementById('input');
            input.click();
        },
        fileChange() {
            let input = document.getElementById('input');
            for(let i = 0; i < input.files.length; i++) {
                file = input.files[i];
                this.loadFile(file);
            }
        },
        loadFile(file) {
            let url = URL.createObjectURL(file);
            let type = file.type;
            console.log(type)
            let name = file.name;
            let video = {
                name: name,
                type: type,
                url: url,
                file: file,
                percentage: 0,
                top: 100,
                status: 'uploading'
            }
            this.videos.push(video);
        },
        async beginUpload() {
            for(let i = 0; i < this.videos.length; i++) {
                let video = this.videos[i];
                if(video.status != 'success') {
                    await this.uploadVideo(video);
                }
            }
            let allSuccess = true;
            let failVideos = [];
            for(let i = 0; i < this.videos.length; i++) {
                let video = this.videos[i];
                if(video.status != 'success') {
                    allSuccess = false;
                    failVideos.push(video);
                }
            }
            if(allSuccess) {
                this.allSuccess = allSuccess;
                this.$notify({
                    title: '上传成功',
                    message: '所有视频已经上传完毕',
                    type: 'success',
                    duration: 0
                  });
            } else {
                console.log(failVideos);
                this.$notify.error({
                    title: '错误',
                    message: failVideos.length+'个视频上传失败，请尝试再次上传',
                    duration: 0
                });
            }
        },
        uploadVideo(video) {
            let param = new FormData();
            param.append('file', video.file);
            video.top = 0
            video.status = 'uploading'
            return axios({
                url: '/edit/upload',
                method: 'post',
                headers: {
                    'Content-Type':'multipart/form-data'
                },
                data: param,
                onUploadProgress: function(event) {
                    if(event.lengthComputable) {
                        let percent = Math.floor(event.loaded / event.total * 100);
                        window.console.log(percent);
                        video.percentage = percent;
                    }
                },
            })
            .then(res => {
                let data = res.data;
                this.filenames.push(data.filename);
                video.status = 'success';
            })
            .catch(error => {
                window.console.log(error);
                video.status = 'exception';
            });
        },
        beginPreprocess() {
            this.loading = true;
            let that = this;
            axios.post('/edit/video-cloth-ads/preprocess',{
                filenames: this.filenames,
                filter: this.filter
            })
            .then(res => {
                that.loading = false;
                let data = res.data;
                let taskId = data.taskId;
                window.location.href = `/edit/video-cloth-ads/preprocess/${taskId}`
            })
            .catch(e => {
                window.console.log(e);
            });
        }
    },
    mounted() {
        let input = document.getElementById('input');
        input.onchange = this.fileChange;
    }
})