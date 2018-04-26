from allauth.account.decorators import verified_email_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
# Create your views here.
from . import models


def index(request):
    polls=models.Poll.objects.all()

    template=get_template('index.html')
    html=template.render(context=locals(),request=request)
    return HttpResponse(html)

@login_required
# @verified_email_required
def poll(request,pollid):
    try:
        poll=models.Poll.objects.get(id=pollid)
    except:
        poll=None
    if poll:
        pollitems=models.PollItem.objects.filter(poll=poll).order_by('-vote')

    template=get_template('poll.html')
    html=template.render(context=locals(),request=request)
    return HttpResponse(html)

@login_required
# @verified_email_required
def vote(request,pollid,pollitemid):
    try:
        pollitem=models.PollItem.objects.get(id=pollitemid)
    except:
        pollitem=None
    if pollitem:
        pollitem.vote=pollitem.vote+1
        pollitem.save()
    target_url='/poll/'+pollid
    return redirect(target_url)