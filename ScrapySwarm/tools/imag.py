# -*- coding=utf8 -*-
"""
    异步任务类
"""
import logging
import requests
from celery import Celery

def download_pic(image_url, image_path):
    """异步下载图片

    Args:
        image_url (string): 图片链接
        image_path (string): 图片路径
    """
    if not (image_url and image_path):
        return

    try:
        image = requests.get(image_url, stream=True)
        with open(image_path, 'wb') as img:
            img.write(image.content)
    except Exception as exc:
        print(exc)

