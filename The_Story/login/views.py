from django.shortcuts import render, redirect
from django.http import HttpResponse
from login.models import Story, Post
from django.contrib.auth.models import User, auth
from django.contrib import messages
import json
# Create your views here.


def register(request):
    return render(request, 'register.html')


def loginForm(request):
    return render(request, 'login.html')


def home(request):
    data = Post.objects.all()
    story = Story.objects.all()
    result = Story.objects.values()
    list_result = [x for x in result]
    text1 = list_result[0]['text1'].split(',')
    text2 = list_result[0]['text2'].split(',')
    new_text = []
    print(list_result)
    print(text1, text2)
    for i in range(len(text1)):
        new_text.append(text1[i])
        new_text.append(text2[i])
    return render(request, 'homepage.html', {'posts': data, 'story': story, 'text1': text1, 'text2': text2, 'num': len(text1), 'looptimes': range(2), 'new_text': new_text})

    # return render(request, 'homepage.html', {'posts': data})


def readpage(request):
    story = Story.objects.all()
    result = Story.objects.values()
    list_result = [x for x in result]
    text1 = list_result[0]['text1'].split(',')
    text2 = list_result[0]['text2'].split(',')
    new_text = []
    for i in range(len(text1)):
        new_text.append(text1[i])
        new_text.append(text2[i])

    return render(request, 'reader.html', {'new_text': new_text})


def addUser(request):
    username = request.GET['username']
    firstname = request.GET['firstname']
    lastname = request.GET['lastname']
    email = request.GET['email']
    password = request.GET['password']
    repassword = request.GET['repassword']

    if password == repassword:
        if User.objects.filter(username=username).exists():
            messages.info(request, 'UserName นีมีคนใช้แล้ว')
            return redirect('/register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email นี้เคยลงทะเบียนแล้ว')
            return redirect('/register')
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=firstname,
                last_name=lastname
            )
            user.save()
            return redirect('/home')
    else:
        messages.info(request, 'รหัสผ่านไม่ตรงกัน')
        return redirect('/register')


def addstoryform(request):
    return render(request, 'addstory.html')


def savestory(request):
    title = request.GET['title']
    textcharacter1 = request.GET['text1']
    textcharacter2 = request.GET['text2']
    charactername1 = request.GET['namechat1']
    charactername2 = request.GET['namechat2']
    username = request.user.username
    print(title, textcharacter1, textcharacter2,
          charactername1, charactername2)
    obj = Story(
        title=title,
        text1=textcharacter1,
        text2=textcharacter2,
        namechat1=charactername1,
        namechat2=charactername2,
        user=username
    )
    obj.save()
    return redirect('/home')


def login(request):
    data = request.POST
    body = data.dict()
    username = body['username']
    password = body['password']
    # login
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return redirect("/home")
    else:
        messages.info(request, 'ไม่พบข้อมูล')
        return redirect('/loginForm')


def logout(request):
    auth.logout(request)
    return redirect('/home')
