from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

from payment.pages import(
    paymentResults,
    DrawRandom,
    page_sequence
    )


class Results(paymentResults):
    pass
