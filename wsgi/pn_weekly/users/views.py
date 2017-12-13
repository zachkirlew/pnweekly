import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseRedirect, QueryDict, HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect

from users.ImageUploadForm import ImageUploadForm
from users.models import CustomUser

appname = 'PN Weekly'


# display signup page
def signup(request):
    context = {'appname': appname}
    return render(request, 'users/signup.html', context)


# register new user
def register(request):
    email = request.POST['email']
    password = request.POST['password']
    fName = request.POST['first_name']
    lName = request.POST['last_name']
    phone = request.POST['phone']

    user = CustomUser.objects.create_user(
        email=email,
        password=password,
        first_name=fName,
        last_name=lName,
        phone_number=phone
    )

    user = authenticate(request, email=email, password=password)

    request.session['email'] = email
    request.session['password'] = password
    login(request, user)
    return HttpResponseRedirect('/')


# log user in
def user_login(request):
    if 'email' not in request.POST:
        context = {'appname': appname}
        return render(request, 'users/login.html', context)
    else:
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist. Please sign up or try another email")
            return HttpResponseRedirect('/user_login')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            request.session['email'] = email
            request.session['password'] = password
            login(request, user)
            return HttpResponseRedirect('/')

        else:
            messages.error(request, 'Incorrect password! Please try again')
            return HttpResponseRedirect('/user_login')


# check if email is available
def regCheckUser(request):
    email = request.POST['email']
    try:
        member = CustomUser.objects.get(email=email)
        return JsonResponse({'is_available': False})
    except CustomUser.DoesNotExist:
        return JsonResponse({'is_available': True})


# decorator that tests whether user is logged in
def logged_in(function):
    def test(request):
        if request.user.is_authenticated:
            return function(request)
        else:
            return render(request, 'users/not-logged-in.html', {})

    return test


@logged_in
def logout(request):
    request.session.flush()
    return redirect('/')


@logged_in
def account(request):
    return render(request, 'users/account.html')


@logged_in
def edit_account(request):
    if request.method == "PUT":

        id = request.user.id

        user = CustomUser.objects.get(pk=id)

        # if exists, get body data
        put_dict = QueryDict(request.body)

        # edit variables
        user.first_name = put_dict.get('firstName')
        user.last_name = put_dict.get('lastName')
        user.phone_number = put_dict.get('phone')

        # save to database
        user.save()

        return JsonResponse({'status': 'success'})

    else:
        return JsonResponse({'status': 'failure', 'message': "Method not allowed"})


@logged_in
def alerts(request):
    return render(request, 'users/alerts.html')


@logged_in
def edit_alerts(request):
    if request.method == "PUT":

        user_id = request.user.id

        user = CustomUser.objects.get(pk=user_id)

        # if exists, get body data
        putDict = QueryDict(request.body)

        # casting required from JavaScript -> Python
        if int(putDict.get('business')) == 1:
            user.business = True
        else:
            user.business = False

        if int(putDict.get('music')) == 1:
            user.music = True
        else:
            user.music = False

        if int(putDict.get('sport')) == 1:
            user.sport = True
        else:
            user.sport = False

        if int(putDict.get('tech')) == 1:
            user.technology = True
        else:
            user.technology = False

        user.save()

        return JsonResponse({'status': 'success'})

    else:
        return JsonResponse({'status': 'false', 'message': "Method not allowed"})


@logged_in
def upload_pic(request):
    if request.method == 'PUT':
        put, files = request.parse_file_upload(request.META, request)
        request.FILES.update(files)
        request.PUT = put.dict()

        form = ImageUploadForm(request.PUT, request.FILES)
        if form.is_valid():
            user_id = request.user.id

            #_delete_file('media/user_images/' + str(user_id) + '.png')

            user = CustomUser.objects.get(pk=user_id)
            user.model_pic = form.cleaned_data['image']
            user.save()

            return HttpResponse(user.id)
    return HttpResponseForbidden('allowed only via PUT')


# delete file from filesystem
def _delete_file(path):
    if os.path.isfile(path):
        os.remove(path)


@logged_in
def alerts(request):
    return render(request, 'users/alerts.html')
