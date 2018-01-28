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
// console.log(arguments)
var channel_book_id = `${_arguments[0]}`
var url = `http://www.tadu.com/book/${channel_book_id}`

class Parse {
  constructor() {
    this.page = null
    this.browser = null
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
  async getBook() {
    await this.page.goto(url);
    var book_name = await this.page.$eval('#container > div.left > div.bookcover > div > div.book-detail.f-l > h1 > a', el => el.innerText);
    var author_name = await this.page.$eval('#container > div.left > div.bookcover > div > div.book-detail.f-l > ul > li:nth-child(1) > span.mrg > a', el => el.innerText);
    var book_summary = await this.page.$eval('#container > div.left > div.bookcover > div > div.book-detail.f-l > p', el => el.innerText);
    var book_update_time_list = await this.page.$eval('#aboutCatalogue > div.catalog_list_box > div:nth-child(2) > h4', el => el.innerText);
    book_update_time_list = book_update_time_list.split(' ')
    var book_update_time = book_update_time_list[book_update_time_list.length-2].concat(book_update_time_list[book_update_time_list.length-1])
    // book_update_time = book_update_time.join('')
    this.bookMessage = {
      '_id': _arguments[0],
      'book_id': _arguments[1],
      'channel_book_id': _arguments[0],
      'book_name': book_name,
      'book_summary': book_summary,
      'author_name': author_name,
      'book_update_time': book_update_time,
      'chapter_list': [],
    }
    await sleep(1000)
    this.getChapter()
  }
  async getChapter() {
    let chapter_utl = `http://www.tadu.com/book/catalogue/${channel_book_id}`
    await this.page.goto(chapter_utl);
    var chapter_list_em = '#container > div.right > div.detail-chapters > ul > li',
        chapter_name_em = 'h5 > a'
    var book_info = await this.page.evaluate((chapterList_em, chapterName_em)=>{
        return Array.prototype.slice.apply(document.querySelectorAll(chapterList_em)).map((item, key) => {
          const chapter_name = item.querySelector(chapterName_em).innerText
          const chapter_id = item.querySelector(chapterName_em).getAttribute('href').split('/')[3]
          const chapter_order_id = key * 1 + 1
          return {
            chapter_name,
            chapter_id,
            chapter_order_id
          }
        })
    }, chapter_list_em, chapter_name_em);
    this.bookMessage['chapter_list'] = book_info
    let data = await this.bookMessage
    mongoClient.connect(mongo_url, (err, db) => {
      if (err) {
        console.log('连接失败')
      }
      // 写入数据
      db.collection('channel_id:2').insert(data,(err, result) => {
          if(err) {
            console.log('连接失败')
          }
          this.browser.close()
          // 关闭连接
          db.close()
        }
      )
    })
  }  
}

let parse = new Parse()
parse.init()
