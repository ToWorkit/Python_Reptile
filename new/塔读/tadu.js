const puppeteer = require('puppeteer');
var child_process = require('child_process');
var fs = require('fs')
let axios = require('axios')
let qs = require('qs')

function sleep(second) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(' enough sleep~');
        }, second);
    })
}

var url = `http://m.tadu.com/book/382477`

class Parse {
  constructor() {
    this.page = null
    this.browser = null
    this.chapterParamsConent = null
  }
  async init() {
    // 是否显示浏览器
    this.browser = await puppeteer.launch({
      'headless': false,
      // 'executablePath': 'C:/Users/hedy/AppData/Local/Google/Chrome/Application/chrome.exe'
    });
    // 等待页面打开
    this.page = await this.browser.newPage();
    // 设置信息
    const UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36";
    await Promise.all([
        this.page.setUserAgent(UA),
        this.page.setJavaScriptEnabled(true),
        this.page.setViewport({width: 1100, height: 1080}),
    ]);
    // 章节内容
    // this.getChapter()
    // 图书信息
    this.getBook()
  }
  // 获取图书信息
  async getBook() {
    await this.page.goto(url);
    let page = await this.page
    // console.log(page)
    // 获取请求完成的信息
    page.on('requestfinished', request => {
      if (request.resourceType == "xhr") {
        if(request.url.indexOf('http://m.tadu.com/book/guessYouLike') != -1) {
          (async () => {
            // 单本图书详情
            let bookMessage = {
              'book_id': null,
              'book_name': null,
              'book_summary': null,
              'book_end_status': null,
              'book_keywords': null,
              'author_name': null,
              'cover_url': null,
              "book_is_vip": 0,
              "book_published_time": 0,
              'book_update_time': null,
            }
            await sleep(2);
            page.mainFrame().waitForSelector('#content > section.book-intro').then(async () => {
              bookMessage['book_name'] = await page.$eval('#content > section.book-intro > a.book-name', el => el.innerText);
              bookMessage['book_summary'] = await page.$eval('#content > section.book-intro > div.intro > p', el => el.innerText);
              bookMessage['book_keywords'] = await page.$eval('#content > section.book-intro > div.book-type > ul > li', el => el.innerText);
              bookMessage['author_name'] = await page.$eval('#content > section.book-intro > a.book-author', el => el.innerText);
              bookMessage['cover_url'] = await page.$eval('#content > section.book-intro > a.book-cover > img', el => el.src);
              console.log(bookMessage)
              await page.$eval('#content > section.book-catalog > a.more-chapter', el => el.click());
              await sleep(2);
            })
            let chapter = [];
            page.mainFrame().waitForSelector('#container > div.setHeight > section > ul > li').then(async () => {
              let chapter_list = await page.$eval('#container > div.setHeight > section > ul', el => el.innerText);
              chapter.push(chapter_list)
              console.log(chapter_list.split('\n'))
            })
          })()
        }
      }
    });
  }
  // 获取章节
  async getChapter() {

  }
}


let parse = new Parse()
parse.init()
