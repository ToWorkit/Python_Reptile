var child_process = require('child_process');
const puppeteer = require('puppeteer');
const mongodb = require('mongodb')
let request = require('request')
let express = require('express')
let axios = require('axios')
let qs = require('qs')
let app = express()
// 连接的url
const mongo_url = 'mongodb://192.168.0.126:27017/book'
// 数据库操作
const mongoClient = mongodb.MongoClient

// 接收参数 node spider.js <参数>
// 先输入抓取站点的书籍id，在输入咱们站上的书籍id
var _arguments = process.argv.splice(2);
console.log(_arguments)
// child_process.exit(0)

let channel_book_id = _arguments[0]
let url = `https://guofeng.yuedu.163.com/source/${channel_book_id}`
// var chapterParams = {}

// const getWy = params => {return axios.get(`https://yuedu.163.com/getBook.do?id=${arguments}&tradeId=`, {params: params}).then(res => res.data)}
const getWy = params => {return axios.get(`https://guofeng.yuedu.163.com/newBookReader.do?operation=info&sourceUuid=${channel_book_id}&catalogOnly=true`).then(res => res.data)}

class Parse {
  constructor() {
    this.res = null
    // 单本图书详情
    this.bookMessage = {}
  }
  async init() {
    this.getBook()
  }
  // 获取图书信息
  async getBook() {
    // 是否显示浏览器
    this.browser = await puppeteer.launch({
      'headless': false,
    });
    this.page = await this.browser.newPage();
    // 设置信息
    const UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36";
    await Promise.all([
        this.page.setUserAgent(UA),
        this.page.setJavaScriptEnabled(true),
        this.page.setViewport({width: 1100, height: 1080}),
    ]);
    await this.page.goto(url);
    // 获取属性值
    var book_name = await this.page.$eval('#identify > div > h3', el => el.title);
    var author_name = await this.page.$eval('#identify > div > h3 > span > a', el => el.innerText);
    var book_summary = await this.page.$eval('#identify > div > div.description.j-desc', el => el.innerText);
    var book_update_time = await this.page.$eval('#J_chapter > div > div.tab-item.crt > span', el => el.innerText);
    book_update_time = book_update_time.split('：')[1]
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
    this.browser.close()
    await this.getChapter()
  }
  // 获取章节
  async getChapterParams() {
    return new Promise((resolve, reject) => {
      getWy().then(res => {
        this.res = res
        resolve(res)
      })
    })
  }
  // 章节信息
  async getChapter() {
    let book =  await this.getChapterParams()
    this.bookMessage['chapter_list'] = await book.catalog
    this.saveMongo()
  }
  // 保存至mongoDB
  async saveMongo() {
    let data = await this.bookMessage
    mongoClient.connect(mongo_url, (err, db) => {
      if (err) {
        console.log('连接失败')
      }
      // 写入数据
      db.collection('channel_id:57').insert(data,(err, result) => {
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
