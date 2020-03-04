from otree.api import (
    models, widgets,
    BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from payment.models import(
    paymentConstants,
    paymentPlayer
)

author = 'Amma Panin'

doc = """
Payments practice module.
"""

class Constants(paymentConstants):
    name_in_url = 'payment_practice'
    practice = True

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(paymentPlayer):
    pass
