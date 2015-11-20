# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):

    form_model = models.Player
    form_fields = []

    def is_displayed(self):
        return self.subsession.round_number == 1

class UnderstandingQuestions(Page):

    form_model = models.Player
    form_fields = ['understanding_question_1','understanding_question_2','understanding_question_3','understanding_question_4']

    def is_displayed(self):
        return self.subsession.round_number == 1

    def understanding_question_1_error_message(self, value):
        if not (value == 22.5):
            return 'Hint: a total of $50 was contributed to the group. This amount will be multiplied by 1.8 and then divided evenly between the members of the group.'

    def understanding_question_2_error_message(self, value):
        if not (value == 32.0):
            return 'Hint: $108 will be divided evenly between the members of the group.'

    def understanding_question_3_error_message(self, value):
        if not (value == 14.0):
            return 'Hint: you begin with a $20 endowment, contribute $10, receive $5 back, and then sanction another group member at a cost of $1.'

    def understanding_question_4_error_message(self, value):
        if not (value == 10.0):
            return 'Hint: refer to the sixth bullet point in the directions above.'

class UnderstandingQuestionsWaitPage(WaitPage):
    def is_displayed(self):
        return self.subsession.round_number == 1

class Contribute(Page):

    form_model = models.Player
    form_fields = ['contribution']

class ContributeWaitPage(WaitPage):
    pass

class Sanction(Page):
    pass

class SanctionWaitPage(WaitPage):
    pass


page_sequence = [
	Introduction,
	# UnderstandingQuestions,
	# UnderstandingQuestionsWaitPage,
	Contribute,
    # ContributeWaitPage,
    Sanction,
    # SanctionWaitPage,
    RoundResults,
    FinalResults
]