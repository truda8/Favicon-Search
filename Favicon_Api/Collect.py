# encoding: utf-8
import requests
from hashlib import sha1
from time import sleep as time_sleep

def get_sha1(content):
    hash = sha1()
    hash.update(content.encode('utf-8'))
    return hash.hexdigest()

url = "https://api.github.com/search/code?l=&p=%d&q=%s&type=Code&per_page=100"
query = "extension:ico+extension:png+extension:jpg+extension:jpeg+extension:gif+filename:favicon"
username = "your github username"
access_token = "your github access token"
page_number = 100
headers = {
    "Accept": "application/vnd.github.v3+json"
}
# create a re-usable session object with the user creds in-built
gh_session = requests.Session()
gh_session.auth = (username, access_token)
proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'http://127.0.0.1:10809',
}

def run(Mongo):
    print("开始运行...")
    success_num = 0
    total_num = 0
    for page in range(page_number):
        page += 1
        print("获取第%d页..." % page)
        with open("page.txt", "w") as f:
            f.write(str(page))
            
        page_url = url % (page, query)
        response = gh_session.get(url=page_url, headers=headers, proxies=proxies)

        # 获取剩余次数
        x_ratelimit = response.headers.get('X-RateLimit-Remaining')
        if x_ratelimit:
            if x_ratelimit == 0:
                time_sleep(60)
        else:
            time_sleep(60)

        if response.status_code != 200:
            print(response.text)
            continue

        print("获取成功！")
        result = response.json()
        total_count = result.get('total_count')
        total_num += total_count

        # Result processing
        items = result.get('items')
        for item in items:
            try:
                # 获取信息
                file_url = item.get('url')
                file_response = gh_session.get(url=file_url, headers=headers, proxies=proxies)

                # 获取剩余次数
                x_ratelimit = response.headers.get('X-RateLimit-Remaining')
                if x_ratelimit:
                    if x_ratelimit == 0:
                        time_sleep(60)
                else:
                    time_sleep(60)

                if file_response.status_code != 200:
                    print(file_response.text)
                    continue

                file_json = file_response.json()
                content = file_json.get('content')  # base64
                if content:
                    content = str(content).replace("\n", "")
                else:
                    continue

                file_sha1 = get_sha1(content)
                github_html_url = item.get("html_url")

                # 查询记录是否已经存在
                num = Mongo.check(file_sha1, github_html_url)
                if num != 0:
                    continue  # 跳过
                
                # 插入数据
                print("插入数据:", file_sha1, github_html_url)
                insert_result = Mongo.insert(file_sha1, github_html_url)
                if insert_result:
                    print("插入成功：", insert_result)
                else:
                    print("插入失败:", file_sha1, github_html_url)
                if insert_result:
                    success_num += 1
                time_sleep(1)
            except Exception as e:
                print(e)
                continue
        if page * 100 >= total_count:
            break
        
    return success_num, total_num


if __name__ == '__main__':
    import DB
    # init MongoDB
    Mongo = DB.Mongo(db="mongodb://username:password@127.0.0.1/favicon")
    run(Mongo)