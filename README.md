# TweetCLI
Backend for a twitter-like application developed for CS 3251 

Known Issues
------------
getusers : the command getusers must be ran twice before users are returned. for some reason I think the client doesnt send until the second run -> DONE

tweet : - handle hashtag case where there are consecutive tags, ie. #tag1#tag2 -> DONE
        - handle case where there are no hashtags (sorry if i messed this up!) -> tweet will always have a hashtag -> DONE
        
subscribe : - handle dedeuplications (bold section in subscribe() part of pdf) -> DONE

exit : doesnt exist -> 

getTweets : reformat to be like timeline and data doesnt get to client? -> DONE

---

After that I think we just should read the pdf and check that we got everything, check for edge cases, and update this readme


