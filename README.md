# MLB Trade Trees

###  2.0.1 Release: December 30, 2021

## [www.mlbtradetrees.com](http://www.mlbtradetrees.com "www.mlbtradetrees.com") allows you to view the trade tree of any player in MLB history. 

### What is a trade tree? 
A trade tree will show you the complete details of a trade made by a team. Let's use Hall Of Fame candidate Cliff Lee for some examples, as he was traded multiple times throughout his career..

Here is the simplest form of his tree: [![Cliff Lee Phils](https://i.imgur.com/xNO9GWU.png "Cliff Lee Phils")](http://https://i.imgur.com/xNO9GWU.png "Cliff Lee Phils")

Cliff Lee was traded to the Mariners in 2009, and the Phillies received 3 players in return. All players the Phillies received in return either retired or became free agents, ending the tree with them. 

Let's take a look at a more complicated example:

[![Cliff Lee Phils](https://i.imgur.com/Nj8BtQB.png "Cliff Lee Phils")](https://i.imgur.com/Nj8BtQB.png "Cliff Lee Mariners")

We can see the Mariners traded away Cliff Lee in 2010, receiving 4 players in return. 2 Players' lines end due to free agency and being picked up on waivers. 2 players' lines continue due to being traded away the next year. Some of those players' lines end however some continue to be traded away, so the tree grows. The tree finally ends in 2014 due to the final player hitting free agency. 

Some of these trees can get pretty massive, spanning decades and dozens of trades. An example is [Harry Simpson](http://www.mlbtradetrees.com/player/simph101 "Harry Simpson").

## The Database
    
 The information used here was obtained free of
 charge from and is copyrighted by Retrosheet.  Interested
 parties may contact Retrosheet at "www.retrosheet.org".

I have made some adjustments to the database that allows the search to go more smoothly:

### Transaction database (data/sorted_transactions_final.csv)
- Nan players involved in trades were changed to "PTBNL/Cash" (player to be named later). Most of the time you see this in a tree, it is a cash transaction. 
- Transactions of players that were released or granted free agency, then signed back with the team as their next transaction were deleted as it caused trees to end prematurely. 
- Franchise tags were added to the database to ensure that a team name change doesn't end a tree. 

### Team database (data/teams.csv)
- All teams in the database received a franchise tag if they are part of the same franchise. They received a unique franchise code if they are an independant team. 

### Player database (data/players.csv)
- Nothing changed, just made a copy with the full name to easily get the user input from the homepage. (static/css/searchable_players.csv)

## Installing Locally
If you want to run the website locally:
- install flask
- install pandas
- install JSGlue (allows Jinja to work in a js file)

Run server.py


## What am I working on? 
#### Updated Dec. 30 2021
- Adding stat support. I'd like to add total WAR contributed by players in a trade on the tree.

- Searching for and filtering trees based on team, year, players in a tree, length of trees, etc.

- Some players don&#39;t display properly due to having very old teams not listed in the teams database. Usually these are players before 1920. I just need to update the transactions database to find all teams without the franchise tag. 

- Various UI enhancements, like clickable nodes to get a player's tree, collapsable nodes for easier readability. 









