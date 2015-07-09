from django.forms import ModelForm,ChoiceField,Form
from rank.models import VoteEvent,Individual

class EventForm(ModelForm):
    '''イベントのフォーム'''
    class Meta:
        model = VoteEvent
        fields = ('name', )

class IndividualForm(ModelForm):
    '''投票者のフォーム'''
    class Meta:
        model = Individual
        fields = ('member_name', )

class MyForm(Form):
    choice_field = ChoiceField(choices = ([('1','1'), ('2','2'),('3','3'), ]), initial='3', required = True,)
