# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random
import operator
import sys

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'Noah Grumman'

doc = """
A public goods game for testing the effect of social rewards on norm enforcement.
"""


class Constants(BaseConstants):
    name_in_url = 'PublicGoodsGame'
    players_per_group = 4
    num_rounds = 12

    endowment = c(10)
    sanction_fee = c(1)
    sanction_penalty = c(3)
    efficiency_factor = 2

    contribution_reward = c(0.05)
    candy_1 = "Mini-snickers"
    candy_2 = "Starburst"

    paying_round = 2

class Subsession(BaseSubsession):
    def before_session_starts(self):
        if self.round_number == 1:
            num_groups = len(self.get_groups())
            treatments = ['Control','Monetary','Candy']
            treatment_counter = 0
            for group in self.get_groups():
                players = group.get_players()
                for player in players:
                    player.participant.vars['treatment_group_1'] = treatments[treatment_counter % 3]
                    player.participant.vars['treatment_group_2'] = treatments[(treatment_counter + 1) % 3]
                    player.participant.vars['treatment_group_3'] = treatments[(treatment_counter + 2) % 3]
                treatment_counter += 1

class Group(BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    rank_1_contribution = models.CurrencyField()
    rank_2_contribution = models.CurrencyField()
    rank_3_contribution = models.CurrencyField()
    rank_4_contribution = models.CurrencyField()

    def set_preliminary_payoffs(self):
        contributions = [(p,p.contribution) for p in self.get_players()]
        random.shuffle(contributions)
        for entry in contributions:
            entry[0].rank = contributions.index(entry)
            if contributions.index(entry) == 0:
                self.rank_1_contribution = entry[1]
            elif contributions.index(entry) == 1:
                self.rank_2_contribution = entry[1]
            elif contributions.index(entry) == 2:
                self.rank_3_contribution = entry[1]
            elif contributions.index(entry) == 3:
                self.rank_4_contribution = entry[1]

        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            if (self.subsession.round_number in range(1,5) and p.participant.vars['treatment_group_1'] == 'Monetary') or (self.subsession.round_number in range(5,9) and p.participant.vars['treatment_group_2'] == 'Monetary') or (self.subsession.round_number in range(9,13) and p.participant.vars['treatment_group_3'] == 'Monetary'):        
                p.initial_payoff = Constants.endowment - p.contribution + self.individual_share + (Constants.contribution_reward * p.contribution)
            else:
                p.initial_payoff = Constants.endowment - p.contribution + self.individual_share

    def set_final_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        sanctioned = {p.rank : p for p in self.get_players()}
        for p in self.get_players():
            p.num_sanctioned = 0

        for p in self.get_players():
            sanctions = 0
            if p.sanctions_rank_1:
                sanctions += 1
                sanctioned[1-1].num_sanctioned += 1
            if p.sanctions_rank_2:
                sanctions += 1
                sanctioned[2-1].num_sanctioned += 1
            if p.sanctions_rank_3:
                sanctions += 1
                sanctioned[3-1].num_sanctioned += 1
            if p.sanctions_rank_4:
                sanctions += 1
                sanctioned[4-1].num_sanctioned += 1
            p.num_sanctions = sanctions

        for p in self.get_players():
            if (self.subsession.round_number in range(1,5) and p.participant.vars['treatment_group_1'] == 'Monetary') or (self.subsession.round_number in range(5,9) and p.participant.vars['treatment_group_2'] == 'Monetary') or (self.subsession.round_number in range(9,13) and p.participant.vars['treatment_group_3'] == 'Monetary'):
                p.final_payoff = Constants.endowment - p.contribution + self.individual_share - (Constants.sanction_fee * p.num_sanctions) - (Constants.sanction_penalty * p.num_sanctioned)  + (Constants.contribution_reward * p.contribution)
            else:
                p.final_payoff = Constants.endowment - p.contribution + self.individual_share - (Constants.sanction_fee * p.num_sanctions) - (Constants.sanction_penalty * p.num_sanctioned)
            if self.subsession.round_number == Constants.paying_round:
                p.payoff = p.final_payoff

class Player(BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null=True)
    # </built-in>

    treatment_group_1 = models.CharField()
    treatment_group_2 = models.CharField()
    treatment_group_3 = models.CharField()

    contribution = models.CurrencyField(min=0, max=Constants.endowment)
    understanding_question_1 = models.CurrencyField(min=0)
    understanding_question_2 = models.CurrencyField(min=0)
    understanding_question_3 = models.CurrencyField(min=0)
    understanding_question_4 = models.CurrencyField()

    questionnaire_1 = models.CurrencyField(min=0)
    questionnaire_2 = models.CurrencyField(min=0)
    questionnaire_3 = models.IntegerField()
    questionnaire_4 = models.CharField()
    questionnaire_5 = models.IntegerField()
    questionnaire_6 = models.TextField()

    sanctions_rank_1 = models.BooleanField(blank=True,default=False)
    sanctions_rank_2 = models.BooleanField(blank=True,default=False)
    sanctions_rank_3 = models.BooleanField(blank=True,default=False)
    sanctions_rank_4 = models.BooleanField(blank=True,default=False)

    initial_payoff = models.CurrencyField()
    final_payoff = models.CurrencyField()
    rank = models.IntegerField()
    num_sanctions = models.IntegerField()
    num_sanctioned = models.IntegerField()

    def role(self):
        # you can make this depend of self.id_in_group
        return ''

    