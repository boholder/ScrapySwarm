
from django.http import HttpResponse
from django.shortcuts import render
from ScrapySwarm.control.swarm_api import runAllSpider
# Create your views here.

from .models import keyword_statistics as WebData


thread_dict={}


def index(request):
    data = WebData.objects.all()
    return render(request, 'Spider.html', {'data': data,'spiders':thread_dict.keys()})


def test(request):
    return render(request, 'index.html', {'data':None})

def getData(request):
    result = WebData.objects.all()
    data = ''
    for i in result:
        data=data+"<li title=\""+str(i)+"\">"+i["keyword"]+":" +str(i.sum())+"</li>"
    # json返回为中文
    from django.http import HttpResponse
    data=data+"&"
    for i in thread_dict.keys():
        if thread_dict[i].is_alive():
            data = data + "<li>" + i + "</li>"
        else:
            thread_dict[i]=None
    return HttpResponse(data, content_type="application/json,charset=utf-8")


def start_spider(request):
    keyword= request.POST.get("keyword")
    if keyword in thread_dict:
        if thread_dict[keyword]. is_alive():
            return HttpResponse("0")
        else:
            thread_dict[keyword]==None

    t=runAllSpider(keyword)
    thread_dict[keyword]=t
    return HttpResponse("1")
