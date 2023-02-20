var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index/index');
  // res.render('index', { title: 'Express' });
});

// router.get('/1212', function(req, res, next) {
//   res.send({'title': 1121123 })
// });

module.exports = router;
