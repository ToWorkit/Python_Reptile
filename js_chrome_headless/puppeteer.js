const puppeteer = require('puppeteer');
var child_process = require('child_process');
var url = "http://t.shuqi.com/route.php?pagename=#!/ct/chapterList/bid/7041137";



(async () => {
  // 获取命令行中输入的参数
/*      var arguments = process.argv.splice(2);
      console.log(arguments)
      // 暂停，不往下执行
      child_process.exit(0)*/


  try {
    // 是否显示浏览器
    const browser = await puppeteer.launch({
      'headless': false
    });
    // 等待页面打开
    const page = await browser.newPage();
    // 设置信息
    const UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36";
    await Promise.all([
        page.setUserAgent(UA),
        page.setJavaScriptEnabled(true),
        page.setViewport({width: 1100, height: 1080}),
    ]);
/*    page.on('request', request => {
      console.log(request.url)
      console.log(request.method)
      // console.log(request.postData)
      console.log(request.headers)
      child_process.exit(0)
      // if (request.resourceType === 'XHR')
      //   // do something
      //   console.log(request)
    });*/

    // 获取请求完成的信息
    page.on('requestfinished', request => {

      if (request.resourceType == "xhr") {
        // console.log(request.method);
        // console.log(request.url);
        if (request.method == "POST") {
          // console.log(request.postData);
        }
        (async () => {
          let res = await request.response()
          // let result =await res.json();
          let result = await res.text();
          // console.log(result)
          //  const chapter_list = await page.$eval('#page-chapter-list', el => el.innerText);
          //   console.log(chapter_list);

        })()
      }
    });

    await page.goto(url);
    // let content = await page.content();
    //console.log(content);
    let doc = await page.evaluate(() => {
        let res = '';
        let master_menu = document.querySelector('#page-chapter-list > div.chapter-list-content > div > div:nth-child(2)')
        if (master_menu) {
            res = master_menu.innerText;
        }
        return res;
    })
    console.log(doc)
    // let page_content = await page.$eval('#chapterlist', el => el.innerHTML);

    // console.log(page_content);
    
    // 关闭浏览器
    // await browser.close();
  } catch (error) {
    console.log(error)
  }
})();
