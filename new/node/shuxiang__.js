const puppeteer = require('puppeteer')
const mongodb = require('mongodb')
// 连接的url
const mongo_url = 'mongodb://192.168.0.126:27017/book'
// 数据库操作
const mongoClient = mongodb.MongoClient
// 设置等待时间
async function sleep(second) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve('sleep')
    }, second)
  })
}
// 获取控制台输入 node sougo.js <输入值>, 数组格式
// 先输入抓取站点的书籍id，在输入咱们站上的书籍id
let _arguments = process.argv.splice(2);
let url = `http://www.sxyj.net/webapp/book/directory.html?bookid=${_arguments[0].split('_')[1]}`

class Spider {
  constructor() {
    this.browser = null
    // this.page = null
    this.bookMessage = {}
  }
  async main() {
    await this.init()
    await this.getBook()
  }
  async init() {
    // 浏览器
    this.browser = await puppeteer.launch({
      // 显示浏览器
      'headless': false
    });
    // 页面对象
    this.page = await this.browser.newPage();
    // 设置浏览器信息
    const User_Agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Mobile Safari/537.36';
    await Promise.all([
      this.page.setUserAgent(User_Agent),
      // 是否启用js
      this.page.setJavaScriptEnabled(true),
      // 设置页面的大小
      this.page.setViewport({width: 2000, height: 2000})
    ])
  }
  // 书籍信息
  async getBook() {
    let _url = `http://www.sxyj.net/Book_BookDetail/${_arguments[0]}.html`
    await this.page.goto(_url)
    let book_name = await this.page.$eval('#new-book-detail > div > div.message.auto-x > div > h4', el => el.innerText);
    let author_name = await this.page.$eval('#new-book-detail > div > div.message.auto-x > div > ul > li:nth-child(1)', el => el.innerText);
    let book_summary = await this.page.$eval('#Desc', el => el.innerText);
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
    // console.log(this.bookMessage)
    await sleep(2000)
    await this.parse()
  }
  async parse() {
    await this.page.goto(url)
    var chapter_list = await this.page.evaluate((chapterList_em, chapterName_em)=>{
        return Array.prototype.slice.apply(document.querySelectorAll('#book-directory > div.content > div.list > ul li')).map((item, key) => {
          const chapter_name = item.querySelector('span').innerText
          const chapter_id = 0
          const chapter_order_id = key * 1 + 1
          return {
            chapter_name,
            chapter_id,
            chapter_order_id
          }
        })
    });
    // console.log(chapter_list)
    this.bookMessage['chapter_list'] = await chapter_list
    this.saveMongo()
  }
  async saveMongo() {
    let data = await this.bookMessage
    mongoClient.connect(mongo_url, (err, db) => {
      db.collection('channel_id:67').insert(data, (err, result) => {
        if (err) {
          console.log(err, '连接失败')
        }
        // 关闭浏览器
        this.browser.close()
        // 关闭连接
        db.close()
      })
    })
  }
}

let spider = new Spider()
spider.main()
