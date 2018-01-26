const puppeteer = require('puppeteer')
const mongodb = require('mongodb')
// 连接的url
const mongo_url = 'mongodb://192.168.0.126:27017/book',
// 数据库操作
const mongoClient = mongodb.MongoClient,
// 设置等待时间
async function sleep(second) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve('sleep')
    }, second)
  })
}
// 获取控制台输入 node sougo.js <输入值>, 数组格式
let _arguments = process.argv.splice(2);
let url = `http://www.sxyj.net/Book_Chapters/${_arguments[0]}.html`

class Spider {
  constructor() {
    // this.browser = null
    // this.page = null
    this.book_info = {}
  }
  async main() {
    await this.init()
    await this.parse()
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
      this.page.setViewport({width: 1400, height: 1080})
    ])
  }
  async parse() {
    await this.page.goto(url)
    var content= await this.page.$eval('#p-book-chapters > div > div.box', el => el.innerText);
    let book_info = {}
    book_info['book_id'] = 
    book_info['channel_book_id'] = 
    book_info['book_name'] = 
    book_info['book_summary'] = 
    book_info['book_keywords'] = 
    book_info['chapter_list'] = 
    mongoClient.connect(url, (err, db) => {
      db.collection('shuxiang').insert(book_info, (err, result) => {
        if (err) {
          console.log(err)
        } else if (result) {
          console(result)
        }
      })
    })
    console.log(content)
  }
}

let spider = new Spider()
spider.main()
