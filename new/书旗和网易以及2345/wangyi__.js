var child_process = require('child_process');
const puppeteer = require('puppeteer');
const mongodb = require('mongodb')
let request = require('request')
let express = require('express')
let axios = require('axios')
let qs = require('qs')
let app = express()
const mongo_url = 'mongodb://118.190.43.138:27017/book'
const mongoClient = mongodb.MongoClient

var _arguments = process.argv.splice(2);
console.log(_arguments)

let channel_book_id = _arguments[0]
let url = `https://guofeng.yuedu.163.com/source/${channel_book_id}`

const getWy = params => {return axios.get(`https://guofeng.yuedu.163.com/newBookReader.do?operation=info&sourceUuid=${channel_book_id}&catalogOnly=true`).then(res => res.data)}

class Parse {
  constructor() {
    this.res = null
    this.bookMessage = {}
  }
  async init() {
    this.getBook()
  }
  async getBook() {
    this.browser = await puppeteer.launch({
      'headless': false,
    });
    this.page = await this.browser.newPage();
    const UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36";
    await Promise.all([
        this.page.setUserAgent(UA),
        this.page.setJavaScriptEnabled(true),
        this.page.setViewport({width: 1100, height: 1080}),
    ]);
    await this.page.goto(url);
    var book_name = await this.page.$eval('#identify > div > h3', el => el.title);
    var author_name = await this.page.$eval('#identify > div > h3 > span > a', el => el.innerText);
    var book_summary = await this.page.$eval('#identify > div > div.description.j-desc', el => el.innerText);
    var book_update_time = await this.page.$eval('#J_chapter > div > div.tab-item.crt > span', el => el.innerText);
    book_update_time = book_update_time.split('：')[1]
    this.bookMessage = {
      '_id': _arguments[0],
      'book_id': _arguments[1],
      'channel_book_id':  _arguments[0],
      'book_name': book_name,
      'book_summary': book_summary,
      'author_name': author_name,
      'book_update_time': book_update_time,
      'chapter_list': [],
    }
    this.browser.close()
    await this.getChapter()
  }
  async getChapterParams() {
    return new Promise((resolve, reject) => {
      getWy().then(res => {
        this.res = res
        resolve(res)
      })
    })
  }
  async getChapter() {
    let book =  await this.getChapterParams()
    this.bookMessage['chapter_list'] = await book.catalog
    this.saveMongo()
  }
  async saveMongo() {
    let data = await this.bookMessage
    mongoClient.connect(mongo_url, (err, db) => {
      if (err) {
        console.log('连接失败')
      }
      db.collection('channel_id:57').insert(data,(err, result) => {
          if(err) {
            console.log('连接失败')
          }
          this.browser.close()
          db.collection('channel_id:98').insert(data,(err, result) => {
            // 关闭连接
            db.close()
            if(err) {
              console.log('连接失败')
            }
          })
        }
      )
    })
  }
}

let parse = new Parse()
parse.init()
