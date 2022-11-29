from icrawler.builtin import BaiduImageCrawler

crawler = BaiduImageCrawler(storage={"root_dir":"image"}) #ダウンロード先のディレクトリを指定
crawler.crawl(keyword="おっぱい", max_num=10, offset=0) #クロール実行
