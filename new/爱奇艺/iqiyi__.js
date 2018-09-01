const puppeteer = require('puppeteer')
const mongodb = require('mongodb')
const mongo_url = 'mongodb://127.0.0.1:27017/book'
const mongoClient = mongodb.MongoClient
async function sleep(second) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve('sleep')
    }, second)
  })
}
// 先输入抓取站点的书籍id，在输入咱们站上的书籍id
let _arguments = process.argv.splice(2);
// 书籍详情页
let book_url = `http://wenxue.iqiyi.com/book/detail-${_arguments[0]}.html`

class Spider {
  constructor() {
    this.browser = null
    // this.page = null
    this.volume_name = null
    this.bookMessage = {}
    this.chapter_count = 0
    this._chapter_list = []
  }
  async main() {
    await this.init()
    await this.getBook()
  }
  async init() {
    this.browser = await puppeteer.launch({
      'headless': false
    });
    this.page = await this.browser.newPage();
    const User_Agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36';
    await Promise.all([
      this.page.setUserAgent(User_Agent),
      this.page.setJavaScriptEnabled(true),
      this.page.setViewport({width: 1376, height: 1366,})
    ])
  }
  // 书籍信息
  async getBook() {
    await this.page.goto(book_url)
    let book_name = await this.page.$eval('body > div.m-box.m-box-mid.m-specificB > section.m-book-list.m-specific-bk > div > div > h1 > strong', el => el.innerText);
    let author_name = await this.page.$eval('#author > div', el => el.innerText);
    let book_summary = await this.page.$eval('#briefContent > p', el => el.innerText);
    let book_update_time = new Date().getTime()
    this.bookMessage = {
      // 对方站书籍id
      '_id': _arguments[0],
      // 咱们站书籍id
      'book_id': _arguments[1],
      // 对方站书籍id
      'channel_book_id':  _arguments[0],
      // 书名
      'book_name': book_name,
      // 简介
      'book_summary': book_summary,
      // 作者名
      'author_name': author_name,
      // 更新信息
      'book_update_time': book_update_time,
      // 章节 -> 章节名，章节id，序号
      'chapter_list': [],
    }
    await sleep(1000)
    // 点击全部章节
    await this.page.$eval('#catalogAll', el => el.click());
    this.getChapter()
/*    var test = await this.page.evaluate(()=>{
      let disabled_class = document.querySelector('div[next="2"]')
      return disabled_class
    })*/
    // console.log(this.bookMessage)
/*    await sleep(2000)
    await this.parse()*/
  }
  async getChapter() {
    var chapter_list = await this.page.evaluate(()=>{
        var volume_order_id = 0;
        return Array.prototype.slice.apply(document.querySelector('#overAll').children).map((item, key) => {
          if (!item.querySelector('a')) {
            this.volume_name = item.innerText
            volume_order_id += 1
            this.chapter_count = 0
          } else {
            var chapter_name = item.querySelector('strong').innerText
            this.chapter_count += 1
            var chapter_order_id = this.chapter_count
          }
          const chapter_id = 0
          // const chapter_order_id = key * 1 + 1
          var volume_name = this.volume_name
          return {
            volume_name,
            volume_order_id,
            chapter_name,
            chapter_id,
            chapter_order_id
          }
        })
    });
    this._chapter_list.push(chapter_list)
    let disabled_class = await this.page.$eval('body > div.m-box.m-box-mid > div.m-bottom-catalog > div:nth-child(3)', el => el.getAttribute('class'));
    if (disabled_class.indexOf('disabled') == -1) {
      await sleep(1000)
      await this.page.$eval('body > div.m-box.m-box-mid > div.m-bottom-catalog > div:nth-child(3)', el => el.click())
      this.getChapter()
    } else {
      this.bookMessage['chapter_list'] = this._chapter_list
      this.saveMongo()
    }
  }
  async saveMongo() {
    let data = await this.bookMessage
    mongoClient.connect(mongo_url, (err, db) => {
      db.collection('channel_id:77').insert(data, (err, result) => {
        if (err) {
          console.log(err, '连接失败')
        }
        this.browser.close()
        db.close()
      })
    })
  }
}

let spider = new Spider()
spider.main()
