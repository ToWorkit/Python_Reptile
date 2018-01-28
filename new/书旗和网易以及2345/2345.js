const puppeteer = require('puppeteer');
var child_process = require('child_process');

function sleep(second) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
        resolve(' enough sleep~');
    }, second);
})
}

var arguments = process.argv.splice(2);
//console.log(arguments)
var book_id = `${arguments[0]}`
var chapter_list_url = `http://book.km.com/chapterlist/${book_id}.html`
var promotion_type = arguments[1]
var book_info = {};

(async ()=>{
    try{
        // 是否显示浏览器，false显示，true不显示
        var browser = await puppeteer.launch({
          'headless': false,
        });
        // 等待页面打开
        var page = await browser.newPage();
        // 设置信息
        const UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36";
        await Promise.all([
            page.setUserAgent(UA),
            page.setJavaScriptEnabled(true),
            page.setViewport({width: 1100, height: 1080}),
        ]);
        // 书籍信息
        var book_info_url=`http://book.km.com/shuku/${book_id}.html`
        await page.goto(book_info_url);
        // 使用document的方式
        var book_info = await page.evaluate(()=>{
            var book_name = document.querySelector("#xtopjsinfo > div.container.clearfix > div > div.col_a > div.abook.clearfix > div.tit_bg > h2").innerText;
            var des = document.querySelector("#xtopjsinfo > div.container.clearfix > div > div.col_a > div.abook.clearfix > div.summary > p.desc").innerText;
            return {
                "des":des,
                "book_name":book_name
            }
        });
        console.log(book_info);
        // 章节列表
        await page.goto(chapter_list_url);
        // 使用css选择器的方式
        var content= await page.$eval('#xtopjsinfo > div.wrapper > div.container > div.catalog > div.catalog_bd', el => el.innerText);
        console.log(content);
    }catch(e){
        console.log(e)
    }
})()



