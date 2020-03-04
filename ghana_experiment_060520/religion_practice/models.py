from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from religion_session.models import (
    religionConstants,
    religionPlayer
    )


author = 'Amma Panin'

doc = """
App is a copy of the main religion_session module
name_in_url is redefined
"""


class Constants(religionConstants):
    name_in_url = 'religion_practice'
    practice = True

class Subsession(BaseSubsession):
    ## Everything of relevance is created at the session level
    ## by religion_session.models.Subsession
    pass


class Group(BaseGroup):
    pass


class Player(religionPlayer):
    pass    
