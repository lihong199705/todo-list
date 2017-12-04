# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from serializers import ThingSerializer
from rest_framework.parsers import JSONParser
from models import Thing


def redictlogin(request):
    return redirect('/accounts/login/')

def redictindex(request):
    return redirect('/todolist/')

def myindex(request):
    data = Thing.objects.all()
    return render(request, 'index.html', {'data': data})


def get_msg(request):
    if request.method == 'GET':
        question = Thing.objects.all()
        serializer = ThingSerializer(question, many=True)
        return JsonResponse(serializer.data, safe=False, status=201)
    return HttpResponse(status=404)


@csrf_exempt
def add_msg(request):
    if request.method == 'POST':
        msg = JSONParser().parse(request)
        serializer = ThingSerializer(data=msg)
        # print serializer.is_valid()
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
    return HttpResponse(status=400)


def del_msg(request, pk):
    if request.method == 'GET':
        Thing.objects.filter(id=pk).delete()
        return JsonResponse({'complete': True}, safe=False)
    return HttpResponse(status=404)


@csrf_exempt
def edit_msg(request, pk):
    if request.method == 'POST':
        msg = JSONParser().parse(request)
        item = Thing.objects.filter(id=pk)
        item.update(
            task=msg.get('task', item[0].task),
            complete=msg.get('complete', item[0].complete),
            # task=msg['task'],
            # complete=msg['complete'],
        )
        return JsonResponse(msg, safe=False)
    return HttpResponse(status=404)