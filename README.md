# WA2-dateapp
H2 computing WA2 Webapp 2024 --> Dating Site

#Inspiration 
This project was inspired by my friend who wants a girlfriend but

#What this project does: 
This project allows a user to find others via the matches tab or recommendations based on tags on that users account and comes with customisable features such as profile pictures and about me

The customisable features of this app allow people to have the ability to give their best first impression of themselves to others to get a higher chance of matches and to help users have more information before matching If a successful match is made, only then can the user check their matches profile which will reveal the match's socials then they can get into contact If a user has tags 'gamer,mugger,joker' and another user has tags 'chill,valorant,gamer' they are likely to end up in each others recommendations due to the similar tag 'gamer'.

#Why is this project useful: 
This webapp provides a platform meeting new people with similar interests. This app can also be used to find friends. The app's main goal is to connect strangers so on it, there is no need to beat around the bush as everyone this app has one thing in common and that is everyone is looking for other people to connect with making users feel more comfortable to be more straight forward

#How it's built
Its built using a database with 3 tables, user information, user account features and match handler. User information is used in login and register. It works with session to ensure that only grants users access to certain pages once logged in. For example, User A who is not matched with User B will not be able to check User B's profile. 

User account features is used in nearly every page e.g. profile, find, matches, e.t.c. It contains all the custom features and loads it into various pages. 

Match handler has 3 columns, user_id, accepted, sent. If A sends B a request, user_id of A will be appended to B's sent and B's user_id will be appended to A's accepted. The idea of this is since A has sent B a request, You have essentially accepted them if they send you a request. B will now have A in his sent list. If A is in both B's sent and accepted column, then they are a Match!


#How to use this webapp:
1. Register
2. Click settings. Set up your about me, tags, profile picture, social links. Include your interests in Tags to find others with same tags
3. Click Find and find someone you want to match with. People who you have sent matches but not accepted your request yet can be seen in Matches > Pending. Or go to Matches > Requests and accept any matches you want to accept.
4. Check Matches for your successful matches.
5. Check your Matches' profile
6. Contact them using their socials
7. Have Fun!

#Accomplishments
JS - I used it to create a slideshow
Database - The python file uses a lot of sqlite3. This webapp allowed me to reinforce my knowledge on databases and I learnt how to use variables in sql commands in python,
Session - I learnt how to use session to pass on data from one page to another. In this website, I used session for two things, session["username"] and session["user_id"]. Session data is only submitted upon a successful login. This ensures that unlogged in users are not granted logged in permissions. It also is used in conjunction with sqlite3. I used it to fetch data depending on session["username"] and session["user_id"].
OS - I learnt how to enable users to submit their own files. In this website, users are able to submit their own profile pictures which is then saved in /static/pfps
CSS - I learn alot more about CSS. I learnt how to use display: flex;

#What's next for the CCA webapp
A chat feature is next for this webapp such that users can communicate on the web app instead of needing to add each other externally on other platforms such as Instagram. Improving of the recommendations algorithm. A random feature to randomly chat with people. In this random feature no information will be disclosed about each other and you can decide to match or not based on talking to them alone.
