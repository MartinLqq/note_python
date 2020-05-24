from datetime import datetime
from pathlib import Path

from matplotlib.pyplot import axis as plt_axis
from matplotlib.pyplot import imshow as plt_imshow
from matplotlib.pyplot import show as plt_show
from jieba import cut as jieba_cut
from requests import get

from bs4 import BeautifulSoup
from wordcloud import WordCloud

from .db import Connection

FONT_PATH = "../fonts/STZHONGS.TTF"
UA = ('Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit/537.36 '
     '(KHTML, like Gecko)Chrome/55.0.2883.87 Safari/537.36')
CLASS_ = "list14"


def spider(url):
    resp = get(url, headers={'User-Agent': UA})
    try:
        html = resp.content.decode()
    except UnicodeDecodeError:
        html = resp.content.decode('gb2312')
    parse_and_save(html)


def parse_and_save(html):
    conn = Connection()
    soup = BeautifulSoup(html, "html.parser")
    for news in soup.find_all(class_=CLASS_):
        titles = news.text.strip()
        for title in titles.splitlines():
            conn.insert(title)
    conn.close()


def plot_img():
    conn = Connection()
    words_list = conn.query()
    conn.close()
    for i, j in enumerate(words_list):
        print('{}. {}'.format(i, j))

    segment = []
    segs=jieba_cut("\n".join(words_list))
    for seg in segs:
        if len(seg)>1 and seg !='\r\n':
            segment.append(seg)

    # img = Image.open(r'../images/Eye.jpg')
    # img_array = array(img)
    wordcloud=WordCloud(
        background_color='black',
        width=1000,
        height=800,
        max_words=100,
        # mask=img_array,
        font_step=1,
        font_path=FONT_PATH,
    )
    # wordcloud.generate("\n".join(wordList))
    wordcloud.generate(" ".join(segment))
    plt_imshow(wordcloud)
    plt_axis('off')
    plt_show()

    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    out_dir = Path('output')
    out_dir.mkdir(exist_ok=True)
    img_path = out_dir / '{}.png'.format(now)
    wordcloud.to_file(img_path)
