# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from API import DB, hash, GetImage
import re


app = Flask(__name__)
app.config.from_object("config.Config")  # import config
Mongo = DB.Mongo(db=app.config.get("MONGODB"))


@app.route('/api/search', methods=['POST'])
def search():
    form = request.get_json(silent=True)
    response = {"status": 200, "msg": ""}
    input_sha1 = ""
    if "upload_image" in form:  # upload image
        upload_image = form.get('upload_image')
        upload_image_list = upload_image.split(",")
        if len(upload_image_list) == 2:
            upload_image = upload_image_list[1]
        else:
            response = {"status": 400, "msg": "Image content is error!"}

        if upload_image:
            input_sha1 = hash.get_sha1(upload_image)
        else:
            response = {"status": 400, "msg": "Image content is empty!"}
    elif "favicon_url" in form:  # input favicon url
        favicon_url = form.get('favicon_url')
        is_url = re.match(r'^https?:/{2}\w.+$', favicon_url)
        if not is_url:
            response = {"status": 400, "msg": "The entered favicon url is incorrect."}

        try:
            result = GetImage.get_content(favicon_url)
        except:
            result = {"status": False, "msg": "Favicon acquisition failed."}

        if result['status']:
            input_sha1 = hash.get_sha1(result['content'])
        else:
            response = {"status": 400, "msg": result['msg']}
    else:
        response = {"status": 400, "msg": "No favicon entered."}

    if input_sha1:
        result = Mongo.query(sha1=input_sha1)

        github_urls = []
        i = 1
        for item in result:
            github_urls.append(item['github'])
            if i >= 8:  # Get up to 8 records
                break
            i += 1
        response['urls'] = github_urls
        response['msg'] = "search success"
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
