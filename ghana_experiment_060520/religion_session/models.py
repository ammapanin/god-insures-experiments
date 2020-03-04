from otree.api import (
    models, widgets,
    BaseConstants, BaseSubsession,
    BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import string
import random
import inspect


author = 'Amma Panin'

doc = """
oTree application for the decision making section of the Ghana church and
insurance paper.

models.py defines the allocations page, and the instructions.

The 'religion_session' app is followed by the payments app.

It is imported to create a practice section.
"""

## Define some general variables, including text for the different
## recipients.

money_space = " <strong>{} ghs </strong> "

keep = "keep" + money_space + "for yourself"
chnm = "give" + money_space + "to your own church with your name"
chur = "give" + money_space + "to your own church anonymously"
thks = "give" + money_space +  "to the thanksgiving offering"
stre = "give" + money_space +  "to the street children's fund"

choice_options = [('A', (keep, chur)),
                  ('B', (keep, chnm)),
                  ('C', (keep, stre)),
                  ('D', (keep, thks)),
                  ('E', (chur, chnm)),
                  ('F', (chur, stre)),
                  ('G', (chur, thks)),
                  ('H', (chnm, stre)),
                  ('I', (chnm, thks)),
                  ('J', (stre, thks))]

choice_options = choice_options

n_choice_pairs = len(choice_options)

letters = list(string.ascii_uppercase)
choice_letters = letters[0: n_choice_pairs]

round_names = ["choice{}".format(i)
               for i in choice_letters]

class religionConstants(BaseConstants):
    players_per_group = None
    num_rounds = n_choice_pairs
    choice_param_dic = dict(zip(round_names,
                                [i[1] for i in choice_options]))
    endowment = 19
    showup_fee = 30
    keep_text = keep
    church_named_text = chnm
    practice_text = "{This is a practice round}"
    n_practice = 3

    class Meta:
        abstract = True

        
class Constants(religionConstants):
    practice = False
    name_in_url = "religion_session"
    
class Subsession(BaseSubsession):

    def creating_session(self):      
        if self.round_number == 1:
            round_nums = range(1, Constants.num_rounds + 1)

            for p in self.get_players():
                round_names = list(Constants.choice_param_dic.keys())
                random.shuffle(round_names)
                
                round_dic = dict(zip(round_nums,
                                     round_names))

                letter_to_round_dic = dict(zip(round_names,
                                               round_nums))

                # Define things in pvars to be used in payments app
                # and across practice and real sessions
                
                pvars = p.participant.vars
                
                pvars['round_dic'] = round_dic
                pvars['letter_to_round_dic'] = letter_to_round_dic
                pvars['choice_dic'] = {}
                pvars['choice_param_dic'] = Constants.choice_param_dic
                pvars['endowment'] = Constants.endowment
                pvars['keep_text'] = Constants.keep_text
                pvars['church_text'] = chur
                pvars['church_name_text'] = chnm
                pvars['thanks_text'] = thks
                pvars['street_text'] = stre
                pvars['showup_fee'] = Constants.showup_fee
                pvars['practice'] = True
                pvars['practice_text'] = Constants.practice_text
                pvars['n_practice'] = Constants.n_practice
              
class Group(BaseGroup):
    pass


class religionPlayer(BasePlayer):
    allocation = models.IntegerField(
        widget = widgets.RadioSelect,
        choices = range(0, Constants.endowment + 1),
        label = None)
    
    member_name = models.StringField(
        label = ("Please enter your name. This will ONLY be used"
                 " if you are giving money to the church with your"
                 " name attached."))
    
    choice_name = models.StringField()
    class Meta:
        abstract = True
        
class Player(religionPlayer):
    pass
  

