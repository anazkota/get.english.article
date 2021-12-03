from re import A
import requests
from bs4 import BeautifulSoup
import nltk
import collections
import pandas as pd

#ここからスタート

#サイト取得　2021-04-20 ~ 2021-12-03のスクリプトを利用（webサイト１ページ分）
response = requests.get("https://transcripts.cnn.com/show/sn")
soup = BeautifulSoup(response.text, "html.parser")


#urlのみ取得,リスト化
links = soup.find_all('a')
url_1 = []
for link in links :
    url_1.append(link.get('href'))

#urlリストいらない要素消す（各々で書き直す）
url_1.pop(0)
url_1.pop(1)
url_1.remove('/')
url_1.remove('/providers')
url_1.remove('?start_fileid=sn_2021-04-20_01')

#リストの要素に'https://transcripts.cnn.com'を追加
url_2 = ['https://transcripts.cnn.com' + n for n in url_1]

#記事を単語に分割
for i in range(len(url_2)):
    url = url_2[i]
    
    #記事のulrからhtmlを取得
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, "html.parser")
    #本文抽出
    cnn10_1 = soup.select(".cnnBodyText")[2]
    
    #記号などを要素から分離
    bun_1 = nltk.word_tokenize(cnn10_1.text)
    
    if i == 0 : url_3 = bun_1
    else : url_3.extend(bun_1)


#各単語の出現頻度を表したものをデータフレーム化
df = pd.DataFrame.from_dict(collections.Counter(url_3), orient='index').reset_index()

#列名変更
df = df.rename(columns={'index':'word', 0:'count'})


#CSVファイルに保存
df.to_csv("")

