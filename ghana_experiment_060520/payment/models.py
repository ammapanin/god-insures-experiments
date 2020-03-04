from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import datetime
from otree import forms
from religion_session.models import religionConstants


author = 'Amma Panin'

doc = """
Payment for the Ghana religion project.
"""

class paymentConstants(BaseConstants):
    players_per_group = None
    num_rounds = 1

    password_practice = "jollofrice"
    password_real = "mysecretpassword"

    endowment = religionConstants.endowment
    
    class Meta:
        abstract = True

class Constants(paymentConstants):
    name_in_url = "payment"
    practice = False

        
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class paymentPlayer(BasePlayer):
    random_letter = models.StringField()
    payment_password = models.StringField(
        label = "Enumerator: please enter password",
        widget = forms.PasswordInput)
    
    enumerator_help = models.StringField(
        label = "Did an enumerator help with answering the questions?",
        choices = ["Yes", "No"],
        widget = widgets.RadioSelect)
    
    class Meta:
        abstract = True
        
class Player(paymentPlayer):
    pass
