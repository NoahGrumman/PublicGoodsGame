# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random
import operator

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
    num_rounds = 6
    treatment_rounds = range(4,7) # note that rounds are 1-indexed, not zero-indexed

    endowment = c(15)
    sanction_fee = c(1)
    sanction_penalty = c(4)
    efficiency_factor = 1.8

    contribution_reward = c(0.05)
    candy_1 = "Peanut M&M"
    candy_2 = "Swedish Fish"

class Subsession(BaseSubsession):
    def before_session_starts(self):
        if self.round_number == 1:
            num_groups = len(self.get_groups())
            treatments = ['Control','Monetary','Candy']
            treatment_counter = 0
            for group in self.get_groups():
                players = group.get_players()
                for player in players:
                    player.participant.vars['treatment_group'] = treatments[treatment_counter % 3]
                treatment_counter += 1

class Group(BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def set_preliminary_payoffs(self):
        contributions = {p : p.contribution for p in self.get_players()}
        rank_text = ["","second-","third-","fourth-"]
        sorted_contributions = sorted(contributions.items(), key=operator.itemgetter(1), reverse=True)
        for entry in sorted_contributions:
            entry[0].rank = sorted_contributions.index(entry)
            entry[0].rank_text = rank_text[sorted_contributions.index(entry)]

        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
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
            p.payoff = Constants.endowment - p.contribution + self.individual_share - (Constants.sanction_fee * p.num_sanctions) - (Constants.sanction_penalty * p.num_sanctioned)


class Player(BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null=True)
    # </built-in>

    treatment_group = models.CharField()

    contribution = models.CurrencyField(min=0, max=Constants.endowment)
    understanding_question_1 = models.CurrencyField(min=0)
    understanding_question_2 = models.CurrencyField(min=0)
    understanding_question_3 = models.CurrencyField(min=0)
    understanding_question_4 = models.CurrencyField()

    sanctions_rank_1 = models.BooleanField(blank=True,default=False)
    sanctions_rank_2 = models.BooleanField(blank=True,default=False)
    sanctions_rank_3 = models.BooleanField(blank=True,default=False)
    sanctions_rank_4 = models.BooleanField(blank=True,default=False)

    initial_payoff = models.CurrencyField()
    rank = models.IntegerField()
    rank_text = models.CharField()
    num_sanctions = models.IntegerField()
    num_sanctioned = models.IntegerField()

    def role(self):
        # you can make this depend of self.id_in_group
        return ''

    