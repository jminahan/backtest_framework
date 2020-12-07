you'll need to run this to start the mongodb daemon
~/mongodb/bin/mongod

##todo long term
    1. nasdaq stock screener is currently being read as a csv on disk
            I should be able to pull from web
    2. need to catalog trading holidays in consts
    3.i think I can put imports in __init__.py?
    4. the broker should always be working off a queue
    5. im dumb a didn't realize there is a difference between instance variables and class variables -- go through and fix