# -*- coding: utf-8 -*-
# @Time  : 2021-02-09 7:30
import requests
from contextlib import closing
import base64

size_limit = 10240000000  # 接收限制 10MB


def get_content(url):
    image_content = b""
    with closing(requests.get(url, stream=True)) as req:
        if 'content-length' in req.headers:
            if int(req.headers['content-length']) > size_limit:
                return {"status": False, "msg": "content-length too many. content-length:"
                                                + str(req.headers['content-length'])}
            image_content = req.content
        else:
            size_temp = 0

            for line in req.iter_lines():
                if line:
                    size_temp += len(line)
                    if size_temp > size_limit:
                        return {"status": False, "msg": "content-length too many. content-length:"
                                                        + str(req.headers['content-length'])}
                    image_content += line

    if image_content:
        image_b64_content = base64.b64encode(image_content).decode()
        return {"status": True, "msg": "success", "content": image_b64_content}
    else:
        return {"status": False, "msg": "favicon acquisition failed."}
