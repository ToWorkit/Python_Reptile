const puppeteer = require('puppeteer');
var child_process = require('child_process');
var fs = require('fs')
let axios = require('axios')
let qs = require('qs')
const mongodb = require('mongodb')
// 连接的url
const mongo_url = 'mongodb://192.168.0.126:27017/book'
// 数据库操作
const mongoClient = mongodb.MongoClient

function sleep(second) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(' enough sleep~');
        }, second);
    })
}

var _arguments = process.argv.splice(2);
console.log(_arguments)
var channel_book_id = `${_arguments[0]}`
var url = `http://t.shuqi.com/route.php?pagename=route.php#!/ct/cover/bid/${channel_book_id}`
// var promotion_type = _arguments[1]

class Parse {
  constructor() {
    this.page = null
    this.browser = null
    this.chapterParamsConent = null
    this.bookMessage = {}
  }
  async init() {
    // 是否显示浏览器
    this.browser = await puppeteer.launch({
      'headless': false,
    });
    this.page = await this.browser.newPage();
    // 设置信息
    const UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36";
    await Promise.all([
        this.page.setUserAgent(UA),
        this.page.setJavaScriptEnabled(true),
        this.page.setViewport({width: 1100, height: 1080}),
    ]);
    // 图书信息
    await this.getBook()
  }
  // 获取图书信息
  async getBook() {
    await this.page.goto(url);
    let page = await this.page
    // console.log(page)
    page.on('requestfinished', request => {
      if (request.resourceType == "xhr") {
        if(request.url.indexOf('http://walden1.shuqireader.com/webapi/book/info') != -1) {
          (async () => {
            let res = await request.response();
            let result = await res.json();
            let res_data = result.data
            // 单本图书详情
            this.bookMessage = {
              // 对方站书籍id
              '_id': res_data.bookId,
              // 咱们站书籍id
              'book_id': _arguments[1],
              // 对方站书籍id
              'channel_book_id': res_data.bookId,
              // 书名
              'book_name': res_data.bookName,
              // 简介
              'book_summary': res_data.desc,
              // 作者名
              'author_name': res_data.cpName,
              // 更新信息
              'book_update_time': res_data.lastInsTime,
              // 章节 -> 章节名，章节id，序号
              'chapter_list': [],
            }
            await sleep(1000)
            this.getChapter()
          })()
        }
      }
    });
  }
  // 章节信息
  async getChapter() {
    let chapter_url = `http://t.shuqi.com/route.php?#!/ct/chapterList/bid/${channel_book_id}`
    await this.page.goto(chapter_url);
    let page = await this.page
    let _chapter_list = []
    page.on('requestfinished', request => {
      if (request.resourceType == "xhr") {
        if(request.url.indexOf('http://walden1.shuqireader.com/webapi/book/chapterlist') != -1) {
          (async () => {
            let res = await request.response()
            let result = await res.json();
            let chapter_list = result.data.chapterList
            // 单本图书详情
            this.bookMessage['chapter_list'] = chapter_list
            // console.log(await this.bookMessage)
            let data = await this.bookMessage
              mongoClient.connect(mongo_url, (err, db) => {
                // 写入数据
                db.collection('channel_id:37').insert(data,(err, result) => {
                    if(err) {
                      console.log('连接失败')
                    }
                    // 关闭浏览器
                    this.browser.close()
                    // 关闭连接
                    db.close()
                  }
                )
              })
          })()
        }
      }
    });
  }
}

let parse = new Parse()
parse.init()
