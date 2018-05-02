import datetime

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from allauth.account.decorators import verified_email_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
# Create your views here.
from . import models


def index(request):
    # polls=models.Poll.objects.all()
    all_polls=models.Poll.objects.all().order_by('-created_at')
    paginator=Paginator(all_polls,5)
    p=request.GET.get('p')
    try:
        polls=paginator.page(p)
    except PageNotAnInteger:
        polls=paginator.page(1)
    except EmptyPage:
        polls=paginator.page(paginator.num_pages)

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
    # try:
    #     pollitem=models.PollItem.objects.get(id=pollitemid)
    # except:
    #     pollitem=None
    # if pollitem:
    #     pollitem.vote=pollitem.vote+1
    #     pollitem.save()
    # target_url='/poll/'+pollid
    # return redirect(target_url)
    #避免重复投票
    target_url = '/poll/' + pollid
    if models.VoteCheck.objects.filter(userid=request.user.id, pollid=pollid, voteDate=datetime.date.today()):
        return redirect(target_url)
    else:
        vote_rec = models.VoteCheck(userid=request.user.id, pollid=pollid, voteDate=datetime.date.today())
        vote_rec.save()
    try:
        pollitem = models.PollItem.objects.get(id=pollitemid)
    except:
        pollitem = None
    if pollitem:
        pollitem.vote = pollitem.vote + 1
        pollitem.save()
    return redirect(target_url)

@login_required
def govote(request):

    # if request.method == 'GET' and request.is_ajax():
    #     pollitemid=request.GET.get('pollitemid')
    #     try:
    #         pollitem=models.PollItem.objects.get(id=pollitemid)
    #         pollitem.vote+=1
    #         pollitem.save()
    #         votes=pollitem.vote
    #     except:
    #         votes=0
    # else:
    #     votes=0

    #避免重复投票
    if request.method=='GET' and request.is_ajax():
        pollid=request.GET.get('pollid')
        pollitemid=request.GET.get('pollitemid')
        bypass=False
        if models.VoteCheck.objects.filter(userid=request.user.id, pollid=pollid, voteDate=datetime.date.today()):
            bypass=True
        else:
            vote_rec = models.VoteCheck(userid=request.user.id, pollid=pollid, voteDate=datetime.date.today())
            vote_rec.save()
        try:
            pollitem = models.PollItem.objects.get(id=pollitemid)
            if not bypass:
                pollitem.vote+=1
                pollitem.save()
                votes=pollitem.vote
            else:
                votes=0
        except:
            votes=0
    else:
        votes=0
    return HttpResponse(votes)