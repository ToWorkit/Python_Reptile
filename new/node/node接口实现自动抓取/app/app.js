let express = require('express'),
    app = express(),
    tadu = require('../tadu__.js')

app.get('/', (req, res, next) => {
  res.send('Hello World');
});

// 请求_01
app.get('/tadu', (req, res, next) => {
  /*setTimeout(() => {
    // res.send('请求_01 完成');
    res.json({
      code:200,
      userid:123
    });
  }, 1000);*/
  (async () => {
    try {
      await tadu.init(req.query.bookId, 'test')
      res.send('请求_01 完成');
    } catch(err) {
      res.send('err');
    }
  })()
});

app.listen(3000, () => console.log(3000));
