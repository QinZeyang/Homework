import pynlpir
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud
from imageio import imread
text = open('result.txt', 'r', encoding='UTF-8').read().replace('\n', '')
pynlpir.open()
#添加一些自定义词汇
pynlpir.nlpir.AddUserWord('漫威'.encode('utf8'), 'noun')
pynlpir.nlpir.AddUserWord('美队'.encode('utf8'), 'noun')
pynlpir.nlpir.AddUserWord('黑寡妇'.encode('utf8'), 'noun')
pynlpir.nlpir.AddUserWord('钢铁侠'.encode('utf8'), 'noun')
pynlpir.nlpir.AddUserWord('漫威'.encode('utf8'), 'noun')
pynlpir.nlpir.AddUserWord('复联'.encode('utf8'), 'noun')
pynlpir.nlpir.AddUserWord('绿巨人'.encode('utf8'), 'noun')
pynlpir.nlpir.AddUserWord('复仇者联盟'.encode('utf8'), 'noun')
pynlpir.nlpir.AddUserWord('灭霸'.encode('utf8'), 'noun')
pynlpir.nlpir.AddUserWord('睡着'.encode('utf8'), 'verb')
pynlpir.nlpir.AddUserWord('雷神'.encode('utf8'), 'noun')
# 开始分词
temp_words = pynlpir.segment(text, pos_names='parent', pos_english=False)
# 输出词汇
words = []
for j in range(len(temp_words)):
    temp = list(temp_words[j])
    words.append(temp)
for word in words:
    print(word)
print(len(words))

# 删除停用词
stopwords = open("stopwords.txt").read()
cur = 0
total = len(words)
for i in range(len(words)):
    if words[i][0] not in stopwords:
        words[cur] = words[i]
        cur += 1
for i in range(cur, total):
    words.pop()

#计算每个类型的词语出现的频率，并进行可视化
df_words = pd.DataFrame(words, columns=['词汇', '词性'])
print(df_words)

df_distribution = pd.DataFrame(df_words['词性'].value_counts())
df_distribution.rename(columns={'词性': '频数'}, inplace=True)
df_distribution['百分比'] = df_distribution['频数'] / df_distribution['频数'].sum()
#print(df_distribution)

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.subplots(figsize=(15, 10))
df_distribution['频数'].plot(kind='barh')
plt.yticks(size=15)
plt.xlabel('频数', size=15)
plt.xlabel('词性', size=15)
plt.title('词性分布分析', size=25)
plt.show()

#输出每个种类出现频率最高的词语
high_words = ['动词', '动词计数', '名词', '名词计数', '代词', '代词计数', '助词', '助词计数', '副词', '副词计数', '形容词', '形容词计数']
df_top = pd.DataFrame(columns=high_words)

for i in range(0, 12, 2):
    df_top[high_words[i]] = df_words.loc[df_words['词性'] == high_words[i]]['词汇'].value_counts().reset_index()['index']
    df_top[high_words[i + 1]] = df_words.loc[df_words['词性'] == high_words[i]]['词汇'].value_counts().reset_index()['词汇']
print(df_top[['名词','名词计数','动词','动词计数']][:20])

#生成词云
mytext = ' '.join(df_words.词汇)
background = imread('2.jpg')#背景图，任意一张纯色背景即可，但不要太大
wc = WordCloud(font_path="C:/Windows/Fonts/simfang.ttf",
               max_font_size=100, mask=background, max_words=300,
               background_color='white', colormap='rainbow', scale=15)
wc.generate(mytext)
plt.imshow(wc)
plt.axis('off')
wc.to_file('out.jpg')