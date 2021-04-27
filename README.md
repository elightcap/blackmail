# blackmail

Bot to interact with Unbelievaboat for the timed removale of rolls and integrate unbelievaboat money
into the pokernow.club chip ecosystem.

Bot requires read access to text channels and role management on discord side.
You'll need to authorize the bot in the unbelievaboat admin panel to get an API key.
Bot will also need to be escalated to admin in poker, in order to give and take chips.



##Blackmail
The role blackmail is created on the target server, and granted via purchase of an item from the store.
In its current use, the role allows a user to collect money once every 2 hours, however this bot removes
the roll every 2 hours, thus only granting the purchaser one use.  It would be pretty simple to change the
role or the timing of removal.

##Poker Stuff
Provides two main functions
    1. BuyIn - this function takes user input, and if they have enough cash on hand, converts it to the specified 
       amount of chips.  Cost is currently in the ration of $1:2 chip, but again this can very easily be changed.
    2. CashOut - this function takes user input, and if they have an equal to or greater number of chips on hand,
       turns them to cash. Ratio is currently 2 chips:$1, however there is a built-in rake, which takes 10% of cash
       recieved and gives it to the Poker bot.  All these numbers can be pretty easily changed to what someone wants.