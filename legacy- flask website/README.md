# MLB Trade Trees

## [www.mlbtradetrees.com](http://www.mlbtradetrees.com "www.mlbtradetrees.com") allows you to view the trade tree of any player in MLB history. 

###  3.1.0 Release: January 27, 2022

#### Changelog
- Overhaul of stats page.
- Addition of compensation draft picks to make trees even larger. 
- New Retrosheet transaction database (all 2021 transactions) was cleaned and added to the website. Check transaction database info below for all changes made.
- Stat support! All trade now has a stat value, and they are added up to create a total tree value. You can hover over a trade to see detailed stats. See below for more information about stats. 
- Lots of UI changes, including clickable nodes for easier traversal. 
- new stats/ search page for all tree values. www.mlbtradetrees.com/stats
- you can hover over a node to see the complete trade breakdown, Google Org chart kinda sucks so it looks pretty bad. Will update later.

### What is a trade tree? 
A trade tree will show you the complete details of a trade made by a team. Let's use Hall Of Fame candidate Cliff Lee for some examples, as he was traded multiple times throughout his career..

Here is the simplest form of his tree: [![Cliff Lee Phils](https://i.imgur.com/xNO9GWU.png "Cliff Lee Phils")](http://https://i.imgur.com/xNO9GWU.png "Cliff Lee Phils")

Cliff Lee was traded to the Mariners in 2009, and the Phillies received 3 players in return. All players the Phillies received in return either retired or became free agents, ending the tree with them. 

Let's take a look at a more complicated example:

[![Cliff Lee Phils](https://i.imgur.com/Nj8BtQB.png "Cliff Lee Phils")](https://i.imgur.com/Nj8BtQB.png "Cliff Lee Mariners")

We can see the Mariners traded away Cliff Lee in 2010, receiving 4 players in return. 2 Players' lines end due to free agency and being picked up on waivers. 2 players' lines continue due to being traded away the next year. Some of those players' lines end however some continue to be traded away, so the tree grows. The tree finally ends in 2014 due to the final player hitting free agency. 

Some of these trees can get pretty massive, spanning decades and dozens of trades. An example is [Harry Simpson](http://www.mlbtradetrees.com/player/simph101 "Harry Simpson").

## The Database (check tests-edits files for complete breakdown of changes made)
    
 The information used here was obtained free of
 charge from and is copyrighted by Retrosheet.  Interested
 parties may contact Retrosheet at "www.retrosheet.org".

I have made some adjustments to the database that allows the search to go more smoothly:

### Transaction database (data/transac2021cleaned.csv)
- Check "edit_transactions.py" for step by step breakdown of what I changed in the database as outlined here: 
- Nan players involved in trades were changed to "PTBNL/Cash" (player to be named later). Most of the time you see this in a tree, it is a cash transaction. 
- Franchise tags were added to the database to ensure that a team name change doesn't end a tree. 

### Team database (data/teams.csv)
- All teams in the database received a franchise tag if they are part of the same franchise. They received a unique franchise code if they are an independent team. Franchise information was taken from https://www.baseball-almanac.com/teammenu.shtml
### Player database (data/players2022.csv)
- Nothing changed, filtered and made a copy with the full name to easily get the user input from the homepage. (static/css/searchable_players.csv)

## Stats
- The following stats are viewable in a tree- WAR, Games, Plate Appearances, Innings Pitched(outs), Salary. These were all taken from BaseballReference WAR daily files.
- Every trade, the traded with players' and the node player's stats on the traded to team are searched for, for the entirety of the time they are on the new team. It is the same for the players received.
- Salary is calculated from the players' salary ON THAT YEAR ONLY. 


## Installing Locally
If you want to run the website locally:
- install flask
- install pandas
- install JSGlue (allows Jinja to work in a js file)

Run server.py


## What am I working on? 
#### Updated Jan. 27 2022
- Google Org Chart is bad for customization so I want to use a new OrgChart UI. 









