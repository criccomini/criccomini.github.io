h5. WHAT I NEEDED

# Daily game schedules for MLB, NBA, NFL, and NHL (the big four).
# Scores and times for MLB, NBA, NFL, and NHL. Can be delayed a minute or two.

I did a bit of reading, and found a few relevant Quora discussions:

* "What options are there for streaming sports stats APIs?":http://www.quora.com/What-options-are-there-for-streaming-sports-stats-APIs
* "Are there any APIs with game schedules available for NFL, NCAA FB, NBA, NCAA BB, and MLB teams?":http://www.quora.com/Are-there-any-APIs-with-game-schedules-available-for-NFL-NCAA-FB-NBA-NCAA-BB-and-MLB-teams

After some research, I was able to get the data I needed for free via either of two sources: MSNBC or ESPN. Later, I decided that I wanted a more secure/legitimate/reliable method of getting score data, so I switched to a pay service called XML Live Scores. I've decided to document my experience in this post.

I encourage you not to abuse the free APIs by polling them too frequently.

h5. ESPN (FREE)

As I said, when I first started out, I was interested in a free solution. I found a few nice write-ups on how to get the scores from ESPN.

* "http://www.wecodethings.com/blog/post.cfm/free-nfl-live-scores-feed-using-coldfusion-can-be-used-for-nba-ncaa-nhl-golf-scores-feed":http://www.wecodethings.com/blog/post.cfm/free-nfl-live-scores-feed-using-coldfusion-can-be-used-for-nba-ncaa-nhl-golf-scores-feed
* "http://www.dbstalk.com/archive/index.php/t-207334.html":http://www.dbstalk.com/archive/index.php/t-207334.html

It turns out, ESPN has a little app called "BottomLine":http://espn.go.com/bottomline/, which makes HTTP requests to a few endpoints to get live sports data. This data is very easy to parse. Here are a few examples:

* "http://sports.espn.go.com/nfl/bottomline/scores":http://sports.espn.go.com/nfl/bottomline/scores
* "http://sports.espn.go.com/nba/bottomline/scores":http://sports.espn.go.com/nba/bottomline/scores
* "http://sports.espn.go.com/mlb/bottomline/scores":http://sports.espn.go.com/mlb/bottomline/scores
* "http://sports.espn.go.com/nhl/bottomline/scores":http://sports.espn.go.com/nhl/bottomline/scores
* "http://sports.espn.go.com/ncf/bottomline/scores":http://sports.espn.go.com/ncf/bottomline/scores
* "http://sports.espn.go.com/rpm/bottomline/race":http://sports.espn.go.com/rpm/bottomline/race
* "http://sports.espn.go.com/sports/golf/bottomLineGolfLeaderboard":http://sports.espn.go.com/sports/golf/bottomLineGolfLeaderboard
* "http://sports.espn.go.com/wnba/bottomline/scores":http://sports.espn.go.com/wnba/bottomline/scores
* "http://sports.espn.go.com/espn/bottomline/news":http://sports.espn.go.com/espn/bottomline/news

As you can see, the data is just URL encoded values. Everything here is pretty much live.

h5. LEAGUE SITES (FREE)

Each league (NBA, NFL, NHL, MLB) exposes live scores on their website. All of these guys use AJAX, which means it's possible to yank out the call that they're using, and make the call yourself, programmatically. Here are some relevant end points:

* "NBA":http://data.nba.com/data/10s/xml/nbacom/2012/scores/playoffs/series_matchup_us.xml
* "NHL":http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp
* "NFL":http://www.nfl.com/liveupdate/scorestrip/scorestrip.json
* "MLB":http://gd2.mlb.com/components/game/mlb/year_2012/month_05/day_15/master_scoreboard.json

You will have to reverse engineer the format of the data, but it's usually pretty straight forward. I didn't bother with this solution because polling these end points is usually a violation of the terms of service for the respective league, and I didn't want to have a per-league score parser.

h5. MSNBC (FREE)

Another alternative that I found, but have not seen documented anywhere, is to use MSNBC's live scores. Nearly all news outlets have live scores for sports, so all you need to do is find one that's making AJAX calls to refresh the scores, and pull out the URL that they're using. The one with the easiest formatting was MSNBC.

* "MSNBC Scores":http://scores.nbcsports.msnbc.com/ticker/data/gamesMSNBC.js.asp?jsonp=true&sport=MLB&period=20120929

When looking at the MSNBC scores in the browser, make sure to view the source, since they have XML encoded in JSON (sigh).

This is the route that I ended up using for free scores. Unlike ESPN's API, which is a bit clunky, MSNBC provides a nice JSON interface. I polled these scores once every 30 seconds, in rotation (MLB, wait 30s, NBA, wait 30s, NFL, wait 30s, etc). Here's some example code (in Python) to get live scores:

<script src="https://gist.github.com/3805436.js"> </script>

I should note that I'm using a couple of Python libraries for help:

* "pytz":http://pytz.sourceforge.net/
* "ElementTree":http://effbot.org/zone/element-index.htm

Again, this is a violation of their terms of service, so beware.

h5. XML LIVE SCORES (&lt;$300/mo)

These are the guys that I use now. Their API is reasonably reliable, and they are really responsive via e-mail. Strangely, they seem to have two sites:

* "http://xml-livescores.com/":http://xml-livescores.com/
* "http://xml-sportsfeeds.com/":http://xml-sportsfeeds.com/

I contacted them via the first one ("http://xml-livescores.com/":http://xml-livescores.com/), but their API is on the second one. Here's an example of their XML data.

<script src="https://gist.github.com/3805418.js"> </script>

To get the data, an HTTP request is made:

bc. curl http://xml-sportsfeeds.com/xml/baseball/livescore/?key=...

I pay in Euros, via PayPal.

h5. XML TEAM

I spoke with an XML team sales rep, who told me that I could get what I needed using their "FlexSport On Demand":http://www.xmlteam.com/fod/ package, which is their low-end pay-as-you-go package. This would have worked great if I were just interested in scheduling, but since I wanted near-realtime scores, the cost would have been too great. They wanted something like 25c per league score request, which would have worked out to 25c a minute per league.

h5. FANFEEDR ($3500/mo)

Before using MSNBC, I was actually using "FanFeedr":http://developer.fanfeedr.com/. At the time, they provided a free API to get live scores, topics, discussion, roster information, etc. Shortly after I began using the site, though, they began charging a minimum of $3,500 a month. Here's "my discussion with them":http://developer.fanfeedr.com/forum/read/156334.

h5. SPORTS DIRECT (~$4,000/mo)

I got in touch with a guy named John Morash. His response to my inquiry was:

Thanks for getting back to me.  We do have the items that you’re looking for but the cost of our service is much greater than $300/mo.  We’re not at the level of STATS Inc. ($4k+) but feel our product is every bit as good.  We don’t compete on price with some of the low-cost vendors however, so it sounds like there may be another option that’s a better fit for you.

h5. OTHERS

There are some other interesting APIs and sites that I didn't bother looking at. 

* "STATS Inc":http://www.stats.com/ (the big guys)
* "Chalk":http://getchalk.com/
* "MLB Stats":http://getchalk.com/