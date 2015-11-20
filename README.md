# Public Goods Game

## Live site
[grumman-publicgoods.herokuapp.com/](https://grumman-publicgoods.herokuapp.com/)

## About

oTree is a Django-based framework for implementing multiplayer decision strategy games.
Many of the details of writing a web application are abstracted away,
meaning that the code is focused on the logic of the game.
oTree programming is accessible to programmers without advanced experience in web app development.

This repository contains the games; the oTree core libraries are [here](https://github.com/oTree-org/otree-core).

## To start locally

```
git clone git@github.com:NoahGrumman/PublicGoodsGame.git
cd PublicGoodsGame
otree resetdb
otree runserver
```