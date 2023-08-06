import urllib3

url = 'https://www.youtube.com/embed/HbaPCfNay1U'

http = urllib3.PoolManager()

r = http.request('GET', url)

html = r.data.decode('utf-8')

with open('html.txt', 'w', encoding='UTF-8') as f:
    f.write(html)


# import utpy

# url = 'https://www.youtube.com/watch?v=3Q_8lPkJm2M' # video or playlist url
# yt = utpy.Load(url)

# # return all information as dic
# print(yt.data)

# # download video or videos of playlist
# yt.download()