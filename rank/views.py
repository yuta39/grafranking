from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils import timezone
from rank.models import VoteEvent,Individual
from rank.form import EventForm,IndividualForm
from django.views.generic.list import ListView
#from ranking.form import EventForm,IndividualForm

def home(request):
    '''トップページ'''
    return HttpResponse(u'トップページ')

class VoteEventList(ListView):
    '''イベントの一覧'''
    context_object_name='vote_ranking'
    template_name='rank/list.html'
    paginate_by = 4 # １ページは最大2件ずつでページングする

    def get(self, request, *args, **kwargs):
        events = VoteEvent.objects.all().order_by("-startTimeDate")
        self.object_list = events

        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)

def eventList(request):
    '''書籍の一覧'''
    event = VoteEvent.objects.all().order_by('id')
    return render_to_response('rank/list.html',
                                {'events':event},
                                context_instance=RequestContext(request))


def eventRanking(request,event_id):
    '''イベントの投票結果'''
    event = get_object_or_404(VoteEvent, pk=event_id)
    members = event.impressions.all().order_by("id")

    return render_to_response('rank/view.html',
                            {'members':members},
                            context_instance=RequestContext(request))


def eventDel(request, event_id):
    '''イベントの削除'''
    event = get_object_or_404(VoteEvent, pk=event_id)
    event.delete()
    return redirect('rank:eventList')

def eventAdd(request):
    '''イベントの追加'''

    if request.method == "POST":
        event_name = request.POST["name"]
        member_list = request.POST.getlist("member")

        event = VoteEvent.objects.create(name=event_name,startTimeDate=timezone.now())

        for member_name in member_list:
            event.impressions.create(member_name=member_name,votes=0)

        return redirect('rank:eventList')
    else:
        event = VoteEvent()
        event_form = EventForm(instance = event)
        member = Individual()
        member_form = IndividualForm(instance = member)

        return render_to_response('rank/add.html',
                                {'event_form':event_form,'member_form':member_form},
                                context_instance=RequestContext(request))


def eventEdit(request,event_id):
    '''イベントの編集'''
    event = get_object_or_404(VoteEvent, pk=event_id)

    if request.method == 'POST':
        event.name = request.POST["name"]
        event.save()
        members = event.impressions.all().order_by("id")

        for i in range(1,30):
            try:
                #参加者の名前変更処理
                new_name = request.POST["member" + str(i)]
                member = members[i-1]
                member.member_name = new_name
                member.save()
            except KeyError as e:
                #変更ループ終了処理
                break

        #新たに追加された人の登録
        for i in range(1,30):
            try:
                new_name = request.POST["member_add_" + str(i)]
                event.impressions.create(member_name=new_name,votes=0)
            except KeyError as e:
                #変更ループ終了処理
                break

        return redirect('rank:eventList')

    event_form = EventForm(instance=event)
    members = event.impressions.all().order_by('id')

    return render_to_response('rank/edit.html',
                              dict(event_form=event_form,members=members,event_id=event_id),
                              context_instance=RequestContext(request))

def eventVote(request,event_id):
    '''イベントの投票'''
    event = get_object_or_404(VoteEvent, pk=event_id)
    members = event.impressions.all().order_by("id")

    if request.method == "POST":
        for member in members:
            value = request.POST["name_" + str(member.id)]
            member.votes += int(value)
            member.save()
        return redirect("rank:eventList")

    return render_to_response('rank/vote.html',
                            dict(members=members,event_id=event_id),
                            context_instance=RequestContext(request))
