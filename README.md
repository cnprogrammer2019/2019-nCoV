<h1>COVID-19(2019-nCoV)</h1>
目的是通过数学方法对发生于2019年年末中国武汉地区的新型冠状病毒肺炎防疫进行处理，希望能有所帮助
<br>
<p>
<b>数据源：</b>
<br>网络（新浪中国,www.sina.cn）
<br>https://interface.sina.cn/news/wap/fymap2020_data.d.json
<br>数据格式为json
</p>

<p>
<b>运行环境：</b>
<br>Ubuntu 1804 LTS
<br>Python 3.6 + requests + matplotlib
</p>

<p>
<b>IDE：</b>
<br>PyCharm 社区版
</p>

<p>
<b>注意：</b>
<br>数据采集中，历史数据是截止到本日零时，实时数据和历史数据会有差别
<br>可以利用定时方式获取“准实时”数据，例如：
<br>crontab -e
<br>*/1 * * * * cd [path];python3 grab_data_from_sina.py
<br>数据会保存到以下目录：[path]/../data
<br>数据文件名：YYYY-MM-DD hh:mm:ss.json
<br>最新数据文件名：last.json
</p>

<p>
<b>清洗数据：</b>
<br>数据如果采集的太过频繁，数据文件较多，其中很多数据重复，例如从2020年1月28日至2020年1月31日，数据超过3000多个
<br>60 X 24 = 1440
<br>清洗数据目录为项目中:cleandata，分为三个主要目录
<br>list：实时变化
<br>historylist：历史每日变化
<br>worldlist：世界数据变化
<br>使用方法：analyse/terminal/clean_data.py
</p>

<p>
<b>制作图表：</b>
<br>根据最新的数据显示每日更新，并且保存到目录文件中
<br>数据源：cleandata/histroylist/最新的json数据文件
<br>图表文件：chart/[historlist|otherlist]/[[line|bra|]|[china|[bar|line]]]/数据文件中的最后日期
<br>使用方法：analyse/terminal/create_**_[line|bar]_chart.py
<br>图片格式：png, svg
</p>

<p>
<b>显示图表：</b>
<br>根据最新的数据显示每日更新，只显示，不产生图片数据文件
<br>数据源：cleandata/histroylist/最新的json数据文件
<br>使用方法：analyse/visual_data/show_**_chart.py
</p>
