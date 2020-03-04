from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

# mi fi password form Sly, MTN
# 02251849

import datetime
from survey.models import Constants as surveyConstants
from religion_session.models import Constants as generalConstants

author = 'Amma Panin'

doc = """
Login details for Ghana sessions
"""

date_object = datetime.datetime.today()
TODAY = date_object.strftime("%d%m%y")
NOW = date_object.strftime("%H%M")

class Constants(BaseConstants):
    name_in_url = 'login'
    players_per_group = None
    num_rounds = 1
    treatments = ("Insurance",
                  "No insurance",
                  "Insurance information")
    
    session_numbers = ["Test", "Individual"] + [str(i)
                                                for i in range(1, 120)]

    enumerator_names = ["Raphael Atta Botchie",
                        "Dorcas Sowah",
                        "James Agbeko",
                        "Cyprine Ocloo",
                        "Emmanuel Ampah-Williams",
                        "Iddrisu Abdul Ganiyu",
                        "Johannes Anaman",
                        "Emmanuel Kems",
                        "Kelvin Mintah",
                        "David Sarpong Agyei",
                        "Nana Ama Asiedu",
                        "Faustina Bechaiyiri*",
                        "Sylvester Sadekla*",
                        "Amma Panin",
                        "Eva Raiber",
                        "Julie Lassebie"]

    enum_list = ["{} -- {}".format(i, name)
                 for i, name in enumerate(enumerator_names, 1)]

    
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    enumerator = models.StringField(choices = Constants.enum_list,
                                    widget = widgets.Select)
    
    treatment = models.StringField(choices = Constants.treatments,
                                   widget = widgets.Select)
    
    experiment_session = models.StringField(choices =
                                            Constants.session_numbers)
    
    church = models.StringField(widget = widgets.Select,
                                choices = surveyConstants.aog_list)

    revival = models.StringField(widget = widgets.Select,
                                 choices = ["Revival week",
                                            "Regular week"])

    revival = models.StringField(widget = widgets.Select,
                                 label = "Did this person come to the session where they were assigned?",
                                 choices = [
                                     ('Yes, the person was assigned  '
                                      'and came during the assigned week'),
                                     ('The person was assigned, but did '
                                      'not come during the assigned week.'),
                                     ('The person was not assigned to '
                                      'any session this week'),
                                     ('The person was assigned to come '
                                     'this week but there was no '
                                      'randomisation')]
    )
    
    explanation = models.StringField(label = ("Please briefly explain why"
                                              "you are not doing the full "
                                              "experiment"))
    
    experiment_date = models.StringField(
        label = "Date",
        initial = TODAY)

    experiment_time = models.StringField(
        label = "Time",
        initial = NOW)

