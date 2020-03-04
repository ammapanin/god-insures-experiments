from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Additional questions for after the games.
"""

class Constants(BaseConstants):
    name_in_url = 'end_survey'
    players_per_group = None
    num_rounds = 1

    yes = ["Yes", "No"]

    days = ["Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"]
    
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    end_number_churches = models.IntegerField(
        label = ('How many different churches have you been a '
                 'member of during your lifetime?'))
    
    end_last_church_attend = models.StringField(
        choices = Constants.days,
    label = ('When was the last time this week that you '
             'attended a church event?'), 
        widget = widgets.Select)

    end_last_revival = models.StringField(
        choices = Constants.yes,
        label = 'Was it part of a revival week?', 
        widget = widgets.Select)
    
    end_event_donation = models.StringField(
        choices = Constants.yes + ["I'm not sure"],
        label = 'Did you make a donation at this event?', 
        widget = widgets.Select)
    
    end_next_church_attend = models.StringField(
        choices = Constants.days,
        label = ('When is the next time you plan to attend a '
                 'church event?'),
        widget = widgets.Select)
 
    end_next_revival = models.StringField(
        choices = Constants.yes,
        label = 'Will it be part of a revival week?', 
        widget = widgets.Select)
    
    
    end_influence = models.StringField(
        choices = Constants.yes,
        label =('Your group played a lottery at the start of the '
                 'interview (when you picked the paper about '
                 'insurance). Do you think the outcome was influenced by God?'), 
        widget = widgets.Select)
