#Project Overview
The goal of this project is to write a Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.
The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.
This project has two parts: defining the database schema (SQL table definitions), and writing the code that will use it.

#Files
- tournament.sql -- table definitions for this project.
- tournament.py -- implementation of a Swiss-system tournament.
- tournament_test.py -- test cases for tournament.

#Instructions
1. [Install Vagrant and VirtualBox](https://www.udacity.com/wiki/ud197/install-vagrant)
2. Download or clone this project [here] (https://github.com/thuynh8/udacity-swiss-tournament-project.git)
3. Navigate to the project in the terminal, then use the command  `vagrant up` (powers on the virtual machine) followed by `vagrant ssh` (logs into the virtual machine). Once you have executed the vagrant ssh command, you will want to `cd /vagrant` to change directory to the synced folders in order to work on your project, once your `cd /vagrant`, if you type `ls` on the command line, you'll see your tournament folder.
4. Run `psql` followed by `\i tournament.sql` to build and access the database.
5. To run the series of tests defined in this test suite, run the program from the command line `$ python tournament_test.py`. 

#Sources
https://docs.google.com/document/d/16IgOm4XprTaKxAa8w02y028oBECOoB1EI1ReddADEeY/pub?embedded=true
