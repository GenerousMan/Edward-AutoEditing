var express = require('express');
var router = express.Router();
var axios = require('axios');
var mongo = require('mongodb');

// 文件上传解析模块 multer
var multer = require('multer');
// multer的存储设置，存储的地址，存储的命名规则等
var storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, '../uploads');
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + '-' + file.originalname);
    }
});
var upload = multer({storage: storage});

var algorithm_port = 5050;

router.get('/', function(req, res, next) {
    res.render('edit/home');
});

router.get('/select', function(req, res, next) {
    res.render('edit/select');
});

router.post('/upload', upload.single('file'), function(req, res, next) {
    let file = req.file;
    let filename = file.filename;
    res.send({ 'filename': filename });
});

router.get('/video-cloth-ads/upload', function(req, res, next) {
    res.render('edit/video-cloth-ads/upload');
});

router.post('/video-cloth-ads/preprocess', function(req, res, next) {
    let filenames = req.body.filenames;
    let filter = req.body.filter;
    axios.post(`http://127.0.0.1:${algorithm_port}/video-cloth-ads/preprocess`, {
        filenames: filenames,
        filter: filter
    })
    .then(response => {
        let data = response.data
        res.send({
            'taskId': data.taskId
        });
    })
    .catch(error => {
        res.send({ 'error': error.message });
    });
});

router.get('/video-cloth-ads/preprocess/:taskId', function(req, res, next) {
    res.render('edit/video-cloth-ads/preprocess');
});

var client = mongo.MongoClient;

router.post('/video-cloth-ads/get-task-progress', function(req, res, next) {
    let params = req.body;
    let taskId = params.taskId;
    var url = "mongodb://localhost:27017/";
    client.connect(url, { useNewUrlParser: true }, function(err, db) {
        if (err) throw err;
        var dbo = db.db("aliwood");
        var col = dbo.collection("preprocess-progress")
        col.findOne({'taskId':taskId}, (err, doc) => {
            if (err) throw err;
            // console.log(doc)
            res.send(doc);
        });
        db.close();
      });
});

router.get('/video-cloth-ads/match/:taskId', function(req, res, next) {
    res.render('edit/video-cloth-ads/match');
});

router.post('/video-cloth-ads/get-match-result', function(req, res, next) {
    let params = req.body;
    let taskId = params.taskId;
    var client = mongo.MongoClient;
    var url = "mongodb://localhost:27017/";
    client.connect(url, { useNewUrlParser: true }, function(err, db) {
        if (err) throw err;
        var dbo = db.db("aliwood");
        var col = dbo.collection("match-result")
        col.findOne({'taskId':taskId}, (err, doc) => {
            if (err) throw err;
            console.log(doc)
            res.send(doc);
        });
        db.close();
      });
});

router.post('/video-cloth-ads/generate-video', function(req, res, next) {
    let params = req.body;
    let taskId = params.taskId;
    let template = params.template;
    axios.post(`http://127.0.0.1:${algorithm_port}/video-cloth-ads/generate-video`, {
        taskId: taskId,
        template: template
    })
    .then(response => {
        let data = response.data
        res.send({
            'resultId': data.resultId
        });
    })
    .catch(error => {
        res.send({ 'error': error.message });
    });
});

router.post('/video-cloth-ads/create-project', function(req, res, next) {
    let params = req.body;
    let taskId = params.taskId;
    let template = params.template;
    axios.post(`http://127.0.0.1:${algorithm_port}/video-cloth-ads/create-project`, {
        taskId: taskId,
        template: template
    })
    .then(response => {
        let data = response.data
        // var client = mongo.MongoClient;
        // var url = "mongodb://localhost:27017/";
        // client.connect(url, { useNewUrlParser: true }, function(err, db) {
        //     if (err) throw err;
        //     var dbo = db.db("aliwood");
        //     var col = dbo.collection("project")
        //     col.findOne({'taskId':taskId}, (err, doc) => {
        //         if (err) throw err;
        //         console.log(doc)
        //         res.send(doc);
        //     });
        //     db.close();
        //   });
        res.send({
            'projectId': data.projectId
        });
    })
    .catch(error => {
        res.send({ 'error': error.message });
    });
});

router.get('/video-cloth-ads/editor/:taskId/:projectId', function(req, res, next) {
    // let params = req.params;
    // let taskId = params.taskId;
    // console.log(params);
    res.render('edit/video-cloth-ads/editor');
});

router.post('/video-cloth-ads/get-project-info', function(req, res, next) {
    let params = req.body;
    let taskId = params.taskId;
    let projectId = params.projectId;
    let template = params.template;
    axios.post(`http://127.0.0.1:${algorithm_port}/video-cloth-ads/get-project-info`, {
        taskId: taskId,
        projectId: projectId
    })
    .then(response => {
        let data = response.data
        res.send(data);
    })
    .catch(error => {
        res.send({ 'error': error.message });
    });
});

router.post('/video-cloth-ads/save-project-info', function(req, res, next) {
    let params = req.body;
    let taskId = params.taskId;
    let projectId = params.projectId;
    let projectInfo = params.projectInfo;
    axios.post(`http://127.0.0.1:${algorithm_port}/video-cloth-ads/save-project-info`, {
        taskId: taskId,
        projectId: projectId,
        projectInfo: projectInfo
    })
    .then(response => {
        let data = response.data;
        res.send({
            'taskId': data.taskId,
            'projectId': data.projectId
        });
    })
    .catch(error => {
        res.send({ 'error': error.message });
    });
});

router.post('/video-cloth-ads/get-project-preview', function(req, res, next) {
    let params = req.body;
    let taskId = params.taskId;
    let projectId = params.projectId;
    let projectInfo = params.projectInfo;
    axios.post(`http://127.0.0.1:${algorithm_port}/video-cloth-ads/get-project-preview`, {
        taskId: taskId,
        projectId: projectId,
        projectInfo: projectInfo
    })
    .then(response => {
        let data = response.data;
        res.send({
            'taskId': data.taskId,
            'projectId': data.projectId,
            'video': data.video
        });
    })
    .catch(error => {
        res.send({ 'error': error.message });
    });
});

router.post('/video-cloth-ads/save-and-generate', function(req, res, next) {
    let params = req.body;
    let taskId = params.taskId;
    let projectId = params.projectId;
    let projectInfo = params.projectInfo;
    axios.post(`http://127.0.0.1:${algorithm_port}/video-cloth-ads/save-and-generate`, {
        taskId: taskId,
        projectId: projectId,
        projectInfo: projectInfo
    })
    .then(response => {
        let data = response.data;
        res.send({
            'taskId': data.taskId,
            'projectId': data.projectId,
            'resultId': data.resultId
        });
    })
    .catch(error => {
        res.send({ 'error': error.message });
    });
});

router.get('/video-cloth-ads/result/:taskId/:projectId/:resultId', function(req, res, next) {
    // let params = req.params;
    // let taskId = params.taskId;
    // console.log(params);
    res.render('edit/video-cloth-ads/result');
});

router.post('/exhibit/get-videos', function(req, res, next) {
    let params = req.body;
    let name = params.name;
    var url = "mongodb://localhost:27017/";
    client.connect(url, { useNewUrlParser: true }, function(err, db) {
        if (err) throw err;
        var dbo = db.db("aliwood");
        var col = dbo.collection("example")
        col.findOne({'name':name}, (err, doc) => {
            if (err) throw err;
            // console.log(doc)
            res.send(doc);
        });
        db.close();
      });
});

router.post('/exhibit/select-begin', function(req, res, next) {
    let params = req.body;
    let name = params.name;
    let videos = params.videos;
    let selected = params.selected;
    axios.post(`http://127.0.0.1:${algorithm_port}/exhibit/select-begin`, {
        name: name,
        videos: videos,
        selected: selected
    })
    .then(response => {
        let data = response.data
        res.send({
            'taskId': data.taskId
        });
    })
    .catch(error => {
        res.send({ 'error': error.message });
    });

});

router.post('/exhibit/get-results', function(req, res, next) {
    let params = req.body;
    let taskId = params.taskId;
    var url = "mongodb://localhost:27017/";
    client.connect(url, { useNewUrlParser: true }, function(err, db) {
        if (err) throw err;
        var dbo = db.db("aliwood");
        var col = dbo.collection("results")
        col.findOne({'taskId':taskId}, (err, doc) => {
            if (err) throw err;
            res.send(doc);
        });
        db.close();
      });
});

router.post('/exhibit/upload-begin', function(req, res, next) {
    let params = req.body;
    let filenames = params.filenames;
    let filter = params.filter;
    axios.post(`http://127.0.0.1:${algorithm_port}/exhibit/upload-begin`, {
        filenames: filenames,
        filter: filter
    })
    .then(response => {
        let data = response.data
        res.send({
            'taskId': data.taskId
        });
    })
    .catch(error => {
        res.send({ 'error': error.message });
    });

});

module.exports = router;
