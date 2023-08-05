import json
from datetime import datetime

from notedrive.github.utils import upload_data_to_github
from noteread.legado.shelf.base import BookSource, BookSourceCorrect
from noteread.legado.shelf.libs.core import load_from_url
from noteread.legado.shelf.libs.correct import correct_source

book = BookSource(lanzou_fid=4147049)
book_correct = BookSourceCorrect(lanzou_fid=4147049)


def load():
    urls = [

        "https://cdn.jsdelivr.net/gh/bushixuanqi/book-source/%E5%85%A8%E7%BD%91%E9%80%9A%E7%94%A8.json",
        "https://cdn.jsdelivr.net/gh/bushixuanqi/book-source/%E4%B9%A6%E6%BA%90%E5%90%88%E9%9B%86.json",

        "https://gitee.com/z507525872/book-source/raw/master/32yousheng.json",
        "https://gitee.com/jia_to_hui/read-30-preferred-book-source/raw/master/bookSource.json",
        "https://guaner001125.coding.net/p/coding-code-guide/d/booksources/git/raw/master/sources/guaner.json",
        "https://haxc.coding.net/p/booksrc/d/booksrc/git/raw/master/Book3.0Source.json",
        "https://haxc.coding.net/p/booksrc/d/booksrc/git/raw/master/bookSource.json",

        "https://namofree.gitee.io/yuedu3/legado3_booksource_by_Namo.json",
        "https://no-mystery.gitee.io/shuyuan/%E5%85%A8%E7%BD%91%E9%80%9A%E7%94%A8.json",
        "https://olixina.coding.net/p/yuedu/d/source/git/raw/master/bookSource.json",
        "https://pbpobing.coding.net/p/yueduyuan/d/sy/git/raw/master/syhj.json",
        "https://pbpobing.coding.net/p/yueduyuan/d/sy/git/raw/master/yshj.json",
        "https://pbpobing.coding.net/p/yueduyuan/d/sy/git/raw/master/3syhj.json",
        "https://pbpobing.coding.net/p/yueduyuan/d/sy/git/raw/master/3yshj.json",

        "https://shuyuan.miaogongzi.site/shuyuan/1612930793.txt",
        "https://shuyuan.miaogongzi.site/shuyuan/1615385692.txt",
        "https://shuyuan.miaogongzi.net/shuyuan/1617076136.json",
        "https://shuyuan.miaogongzi.net/shuyuan/1617281456.json",

        "https://shuyuan.miaogongzi.net/shuyuan/1617406392.json",
        "https://shuyuan.miaogongzi.net/shuyuan/1619463469.txt",
        "https://shuyuan.miaogongzi.net/shuyuan/1619872864.json",
        "https://shuyuan.miaogongzi.net/shuyuan/1619911647.txt",
        "https://shuyuan.miaogongzi.net/shuyuan/1619967369.json",
        "https://shuyuan.miaogongzi.net/shuyuan/1620929243.json",
        "https://shuyuan.miaogongzi.net/shuyuan/1622744487.json",
        "https://shuyuan.miaogongzi.net/shuyuan/1623355431.json",

        "https://shuyuan.miaogongzi.net/shuyuan/1624832786.json",
        "https://shuyuan.miaogongzi.net/shuyuan/1622509629.json",
        "https://shuyuan.miaogongzi.net/shuyuan/1626191885.txt",
        "https://shuyuan.miaogongzi.net/shuyuan/1626711440.json"
        "https://shuyuan.miaogongzi.net/shuyuan/1626966311.json",
        "https://shuyuan.miaogongzi.net/shuyuan/1627802706.txt",
        "https://shuyuan.miaogongzi.net/shuyuan/1630342495.json",
        "https://shuyuan.miaogongzi.net/shuyuan/1631138099.json",
        "https://shuyuan.miaogongzi.net/shuyuan/1632140979.json",
        "https://shuyuan.miaogongzi.net/shuyuan/1633030418.json",
        "https://shuyuan.miaogongzi.net/shuyuan/1633826458.json",
        "https://shuyuan.miaogongzi.net/shuyuan/1630342495.json",

        "https://slaijie.gitee.io/legado/legado/BookSource210116.json",
        "https://tangguochaotian.coding.net/p/tangguoshuyuan1015/d/tangguo/git/raw/master/exportBookSource.json",
        "https://tianyuzhange.coding.net/p/booksource/d/shuyuan/git/raw/master/2.0shuyuan.json",

        "https://gitee.com/ch4nge/readbook/raw/master/booksource_fl",

        "https://gitee.com/ch4nge/readbook/raw/master/booksource200",
        "https://gitee.com/ch4nge/readbook/raw/master/booksource40",
        "https://gitee.com/YiJieSS/Yuedu/raw/master/bookSource.json",
    ]
    # 替换净化
    urls2 = [
        "https://gitee.com/ch4nge/readbook/raw/master/JHGZ",
        "http://shuyuan.miaogongzi.net/shuyuan/1623124621.txt",
        "http://shuyuan.miaogongzi.net/shuyuan/1623087998.txt",
    ]

    # load
    load_from_url(cate1='1', urls=urls, book=book)
    # load_from_mumuceo(cate1='1', source=SHU_YUAN, book=book)
    # load_from_mumuceo(cate1='2', source=RSS_YUAN, book=book)


def correct():
    # correct
    correct_source(book, book_correct)


def upload():
    # save
    print(book.db_save())


def upload_version(cate1='1'):
    data = book_correct.select(condition={'cate1': cate1})[:1000]
    data = [json.loads(d['jsons']) for d in data]

    data = json.dumps(data)
    repo = 'notechats/notefile'
    git_path = f"notechats/noteread/legado-source-{datetime.now().strftime('%Y%m%d%H%M%S')}.json"

    upload_data_to_github(data, git_path, repo)
    print(f'https://raw.githubusercontent.com/{repo}/master/{git_path}')
    print(f'https://gitee.com/{repo}/raw/master/{git_path}')


load()
# correct()
# print()
print(len(book.select_all()))
print(len(book_correct.select_all()))

# upload()
# upload_version(cate1='1')
# upload_version(cate1='2')
