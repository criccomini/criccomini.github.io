---
layout: post
title:  "Tech exits"
author: chris
image: assets/images/2012-10-22-tech-exits/jacob-townsend-771573-unsplash.jpg
redirect_from:
  - /posts/hadoop/2013-06-14-yarn-with-cgroups/
---

What follows is a brain dump of some things that I've learned about the way that software companies are sold on the public and private market.

## Disclaimer

I am not an expert in any of these areas. This is just a list of things that I've heard, or discussed with people, over the years. This is not meant to substitute the advice of a financial advisor. This post does not reflect the view of my employer, or of anyone other than myself.

## Funding

Most tech companies are funded through a combination of [angel investors](http://en.wikipedia.org/wiki/Angel_investor) and [venture capitalists](http://en.wikipedia.org/wiki/Venture_capital) using a combination of [convertible notes](http://techcrunch.com/2012/04/07/convertible-note-seed-financings/) (early) and [preferred equity](http://www.payne.org/index.php/Startup_Equity_For_Employees) (later). At the very beginning, the founders (usually a team of 1-4 people) use their network to get [pitch meetings](http://bitly.com/bundles/royrod/2) with potential investors.

As an employee of a pre-IPO startup, you're probably going to be [compensated with a combination of salary (money) and stock](https://www.secondmarket.com/education/resource/what-startup-employees-should-know-about-their-equity-2). If you're early enough, you'll get [granted shares](http://www.payne.org/index.php/Startup_Equity_For_Employees#Founder.27s_.2F_Restricted_Stock). If you're joining later on, typically post-series-A, you'll get options (the option to buy your shares at a given price). This distinction is rather nuanced; for more information, see the tax section, below. Typically these shares "vest" over a four year period with a one year cliff. This means that you have to wait 1 year before you get 25% of your options. Then, monthly, after that, you'll receive 1/48th of your total grant for the remaining three years.

There are a number of things that you should consider if you go to work for a pre-IPO startup. When the founders raise money, they're going to start hiring employees. The very first employee (employee #1) will typically be offered a chunk of shares that is equivalent to between 0.5% and 1% of the company's valuation. For example, if a startup raised its seed funding at a 10 million dollar valuation, the first employee could receive $100,000 worth of shares. These shares will be regular (not preferred).

You'll notice that I did not say that the employee will receive X number of shares; I said, "Some number of shares valued at X." This is an important distinction that has a huge psychological impact. When companies fight to hire employees, often times, you'll hear, "Company X offered me 30,000 shares, and company Y offered me 10,000. Obviously, I'm going to join company X." This is a completely non-sensical statement. What if the 30,000 shares are worth $1 each, and the 10,000 shares are worth $100 each? You need to ask companies, at least, the following:

* How many shares are there.
* What are the value of the shares.
* What is your exit strategy.

Using this information, you can determine who is offering you more money, in shares. You can also determine the valuation of the company. For example, if a company has 100 million shares valued at 10 cents each, the company is worth $10 million. The valuation of the company can be extremely important, as you'll see in the acquisition section, below.

It's also worth level setting expectations for potential income from the shares you receive. There are generally three scenarios for a startup. The most likely is that the startup dies. The second most likely is that the startup is acquired. The least likely is that the startup IPOs. The simple fact is that very few companies actually have an exit larger than $100 million dollars. If you are an early stage employee at those companies, you will definitely grow your wealth substantially (between $15 million and $100 million, typically), but this is incredibly rare, even in the valley. Let's continue with the employee #1 scenario above. Let's say that you receive 1% of the company, in shares. A few years later, your company is acquired for $100 million dollars (a fairly large acquisition). You now have $1 million dollars in shares. Are you $1 million dollars richer? No. You owe taxes. Depending on how you handle your grant ([AMT](http://en.wikipedia.org/wiki/Alternative_Minimum_Tax) vs. regular income), and which state you live in (state tax; 10% in California), you'll probably earn about $650,000, after taxes. This is a fantastic chunk of money. Does it mean you'll be flying private jets? No. It means you'll live comfortably, pay your kid's college tuition, and not have to worry about losing your house. The media doesn't tell you this kind of stuff, when it sensationalizes IPOs and acquisitions.

I highly recommend [this Quora post](http://www.quora.com/Startups/When-joining-a-small-startup-15-people-what-are-some-appropriate-questions-to-ask-to-help-determine-the-value-of-your-equity-and-the-potential-of-the-company) and [this Wealthfront post](https://blog.wealthfront.com/startup-employee-equity-compensation/) for further reading.

{% include newsletter.html %}

## Acquisitions

Acquisitions are a hot way to cash out in the valley, these days. Companies like Facebook are [acquihiring](http://www.washingtonpost.com/national/on-leadership/for-tech-companies-like-facebook-and-google-acqui-hiring-present-latest-management-challenge/2012/10/11/9b4a9744-13ab-11e2-be82-c3411b7680a9_story.html) failing startups right and left, and a lot of larger companies are flush with cash after IPO'ing and building up their talent pool.

Acquisitions of small startups generally serve several purposes. In today's competitive hiring environment, acquisitions can be an easy way to get a chunk of good engineers all at once. Additionally, if a startup is competing with a larger company, the company might choose to purchase the startup as a way to protect itself (e.g. Instagram and Facebook). Lastly, and most cynically, an acquisition can be used as a way for VCs to cash themselves out without losing all of their money. Some VCs will use their connections to engineer a purchase of a failing startup that they've invested in, in order to prevent a loss, and save face. I should note, however, that not all acquihires are favorable to VCs.

One other thing to look out for, especially if you work at a startup, is the fact that VCs get [preferred shares](http://www.avc.com/a_vc/2011/07/financing-options-preferred-stock.html). Essentially, this means that they get paid in full, before anyone else. For example, if a VC puts in $1 million, and the company sells for $10 million, the VC gets his initial $1 million back before anyone else sees a dime. In cases where the startup is failing, and likely sells for about what it was valued at when raising capital, this means the employees walk away with almost nothing.

Lastly, you need to consider whether the startup that you're joining has priced themselves out of an acquisition. What I mean by this is, when a company raises a round of funding, they sell shares to investors at a given price. The price per share determines the value of the company at that point in time. For example, if a startup raises $20 million dollars at $20 per share, and they have 100 million total shares, then the company is worth 2 billion dollars (20 * 100 million). You have to ask yourself, can you see a company purchasing this startup for $2 billion? Anything under a sale of $2 billion means that some of the VCs will lose money, and is unlikely to happen, since VCs typically hold veto rights on deals.

More reading [here](http://pandodaily.com/2012/08/25/the-acqui-hire-scourge-whatever-happened-to-failure-in-silicon-valley/), [here](http://daslee.me/quick-thoughts-on-acquihiressoft-landings), and [here](http://papers.ssrn.com/sol3/papers.cfm?abstract_id=2040924). I highly recommend the last one, which is a paper from some professors, examining the practice of acquihiring.

## The IPO

Another way that an employee might reach liquidity with regards to his or her shares is when the company that they work for has a public offering of their shares. In such an event, the company elects to make the shares publicly tradable on a stock exchange, such as the NASDAQ or NYSE.

## S-1 filing

A company that wishes to sell some of their shares on the public market must file an S-1 form with the SEC. These forms tend to follow a fairly standard layout, though they typically contain cover letters and some freedom to write in plain english. Here are some examples:

* [Groupon](http://www.sec.gov/Archives/edgar/data/1490281/000104746911005613/a2203913zs-1.htm)
* [Facebook](http://sec.gov/Archives/edgar/data/1326801/000119312512034517/d287954ds1.htm)
* [Yelp](http://sec.gov/Archives/edgar/data/1345016/000119312511315562/d245328ds1.htm)
* [Google](http://i.i.com.com/cnwk.1d/pdf/ne/2004/google.pdf)

If you work for a company that IPOs, you should get familiar with these documents. They provide the first real insight you'll probably see into all of the financials of your company, as well as who the largest share holders are.

The motivation for selling shares varies from company to company, but generally it's required to grow workforce, stay afloat, for protection (buying competition), etc. All the typical reasons that you can imagine a company might need a chunk of cash.

## Quiet period

After the S-1 is filed, the company enters a quiet period. This is a period of time where the SEC gathers information, makes sure that everyone has access to the same information, and makes the S-1 "effective". During this time, changes to the S-1 will be filed (based on new information that might come available), and employees are required to say absolutely nothing about the company, the filing, etc. Any information that leaks out and is not in the S-1 can result in a lot of bad things happening including firing employees that leaked the information, delaying the IPO, etc. The idea, here, is to make it so that everyone, publicly, has the same amount of information available (to prevent insider trading).

## Repricing

Companies will typically re-price their IPO shares (upwards) in the weeks leading up to the IPO. Usually, this is a result of increased demand from the market makers, but it also serves the purpose of building hype.

## Lockup period

When a company has an IPO, there is typically a period where employees are unable to exercise or trade the shares that they own. This period typically lasts between three and six months from the IPO date. The motivation for this is to provide price stability, and prevent shares from flooding the market too quickly. This means, when a company like Facebook goes public, the employees are not selling their shares immediately, and have no more money in their bank account the day after the IPO than they did the day before. Instead, it's the bankers and VCs that are selling shares early on.

One exception to this rule is that some companies will offer their employees the chance to participate in the offering, itself, even though they are locked up. In this scenario, employees might be given the chance to sell some percentage of shares on the day of the IPO. The caveat here is that the employees will not be selling their shares on the open market. They will be selling them to Wall Street market makers at a reduced price compared to the opening. This is a pretty rare opportunity, I've heard, but it does happen.

## Secondary offering

Sometimes, a company that has gone public will file for a secondary offering. This is, essentially, the opportunity for the company to sell more of its shares on the open market. There are generally two reasons that a company might want to do this:

* To prevent stock volatility when a lock-up period expires.
* To raise more money if the stock is doing well.

You might be wondering how a secondary offering can affect the volatility of a newly IPO'd stock. When a lockup-period expires, a flood of shares that have been illiquid will suddenly become liquid. In the case of Facebook, for instance, [270 million new shares](http://money.cnn.com/2012/08/15/technology/facebook-lockup/index.html) will become available on the market in a single day. On average, 46 million shares of Facebook are traded per day. You can bet that the lockup expiration will have an affect on the share price that day.

To prevent all shares from flooding the market at once, a company can get some of its institutional investors to participate in a secondary offering. In this case, the company and its institutional investors will agree to sell some of their shares to investment bankers at a slight discount to the current market price. These bankers will then be locked up for a further period of time (but get a discount off the current market value). If you compound this with the initial lockup, it means that the company can stage dumping of its shares across a longer timespan (IPO, lock-up expiration, secondary offering), which increases the stability of the stock.

## Blackouts

After a company has gone public, it will go into its normal quarterly announcements, where it'll post it's financials, and any other interesting news, to Wall Street. During the blackout period, which can last anywhere from a few weeks to a couple of months (depending on your company, your individual access to data, etc) employees will not be allowed to trade any of the company's shares (either buying or selling) to prevent insider trading.

One way to get around this is to fill out a [10b5-1](http://en.wikipedia.org/wiki/SEC_Rule_10b5-1) form. This is an SEC form that allows you to set up a pre-made schedule that can execute during blackout periods. You can generally set up pretty sophisticated rules, and work with the broker that your company uses (e.g. E-Trade, Schwab, etc) to get your 10b5-1 in place. Typically, executives use these, since they are almost always blacked out since they know a lot about what's going on, and don't want to risk insider trading.

## Wallstreet

To sell IPO shares, a company typically employs underwriters. Underwriters are basically a group of banks that buy the pre-IPO shares from the company, and then turn around and sell them on the public market. The motivation for this is that the underwriters are the ones that incur risk in the case were there turns out to be no market for the shares (people aren't buying them). In that case, the banks end up holding shares of the company for longer than they'd like.

This has a number of cushy side effects. First, underwriters have a pretty strong strangle-hold on the market, and tend to charge between 5% and 7% for the courtesy of flipping a company's shares. Second, underwriters typically provide pre-IPO shares to some of their important investors. Basically, this tends to be free money (if the IPO has a bump in price on opening day) for people who are generally pretty wealthy already (when was the last time your bank called you to offer you an opportunity in pre-IPO shares?).

Facebook and Google are both interesting cases in this area. An alternative to using the typical under-writing system is to do what's called a dutch auction, which is the route Google took. From [Wikipedia](http://en.wikipedia.org/wiki/Initial_public_offering#Dutch_Auction), "This auction method ranks bids from highest to lowest, then accepts the highest bids that allow all shares to be sold, with all winning bidders paying the same price." This is much more friendly to the company, since they tend to get a price that's closer to what would be offered on the public market. Similarly, because of demand from banks, Facebook was able to play hardball, and threaten to dutch auction, if they did not get their shares underwritten at a much lower percentage. I believe the number that I heard was 1.1% (see [Reuters](http://www.reuters.com/article/2012/03/20/net-us-facebook-ipo-idUSBRE82I15N20120320)), which is virtually unheard of.

## Opening bell

When a company's shares trade for the first time on the market, there is typically a period after the opening bell where the shares are not actually being traded. That is, the "sell" offers are far too high above the "buy" offers. As an example, if a company uses banks as underwriters, the underwriters will sell the shares. After that, its up to the owners of the shares to buy and sell on the open market. If the owners of the shares want to sell for $100 a share, and buyers are only willing to pay $50 per share, the stock isn't traded, and the market is in a stalemate. After some period of time (an hour or two, usually), the market converges (the buy orders come up, and the sell orders come down), and shares begin trading hands.

Generally, on the day of an IPO, if under-writers are used (the common case), one of two things can happen: the shares close up, or the shares close flat.

If the shares close up, this can mean a few things. In general, the press coverage is positive, and it looks like the market believes in the company. It can also mean that the company left money on the table. For example, if a company sells its shares to underwriters at $30 a share, and the underwriters sell the shares on the market at $50, and the shares close at $100 at the end of the first day, it's likely that the company could have sold the shares for a lot more (say $40-$50 a share). If the company had sold the shares for more, they would have more cash in the bank at the end of the day.

If, on the other hand, the shares close flat, it means that the company got as much money as they could out of the market, and their bank accounts are about as high as they could theoretically be. The downside is that the press coverage will generally be a little more negative. It also means that the underwriters likely had to buy back the shares. This is a deal that most underwriters agree to when the company sells them shares. Essentially, only for the day of the IPO, the underwriters are required to buy back any stock that's for sale below the IPO price. This is [precisely what happened with Facebook](http://articles.latimes.com/2012/may/18/business/la-fi-tn-facebook-trading-20120518). Morgan Stanley was forced to buy back shares on the day of the IPO. What this means is that the market believes the shares are worth less than their IPO price, and the underwriter will end up paying more for the stocks than they're worth. The underwriters are then forced to hold the shares until the price comes up, or sell the stock (after the day of the IPO) at a loss.

## Selling shares after an IPO

After the dust settles, the lock-up ends, and the secondary offering does (or does not) happen, employees of the company are left to exercise their options, and sell their shares. For early employees, their options' strike price (the price that employees must pay to buy their shares) is likely relatively low. For example, if you were an early employee, you might get stock options at your company for 50 cents per share. If, post-IPO, the shares are trading at $50 per share, that means that, when you exercise your options, you must pay 50 cents per share (1% of the stock price). For later employees, their strike price is likely much higher, or they simply have restricted stock units (see below).

Wealthfront, again, has two really great posts on [divesting shares](https://blog.wealthfront.com/silicon-valley-new-rich-financial-planning/) and [selling strategies](https://blog.wealthfront.com/should-i-sell-my-stock/). In addition, I also highly recommend [Bogleheads' Guide to Investing](http://www.amazon.com/Bogleheads-Guide-Investing-Taylor-Larimore/dp/0470067365). Most of it is pretty common sense stuff, but it's worth it to read it, and consider your options (no pun intended).

## Restricted stock

In the later stages of a pre-IPO company, and for most larger companies, it's likely that employees will receive restricted stock units (RSUs), rather than options. Unlike options, restricted stock has no strike price; you just get the shares for free. Typically, you will receive far fewer RSUs than you would receive options, but they are far less risky, as you will never be "underwater". The term, "underwater," refers to stock options whose strike price is higher than the current market value of the stock, thus making it almost worthless. For example, if a share can be bought for $30 on the public market, and you hold options that have a strike price of $50, it makes no sense to exercise your option to buy the share at $50, when you could buy it for $30. RSUs don't carry this risk. In terms of valuing RSUs vs options (since some companies offer both), I've heard that Yahoo! employees typically used a 3x multiplier when receiving shares. That is, they would ask for 300 options instead of 100 RSUs. This is just what I've heard, but it seems fairly reasonable. As usual, [see Quora for more information](https://www.quora.com/Whats-better-stock-options-or-RSUs?redirected_qid=37903).

## Taxes

Once you've sold your shares, you'll need to pay taxes. There is typically one major thing to consider when looking at taxes: how much time has passed between the time that you received the shares, and when you sold them. The reason that this is important is because of the [capital gains tax](http://en.wikipedia.org/wiki/Capital_gains_tax). If you hold your shares for more than a year, the income is treated as capital gains, which, in the United States, is currently taxed by the federal government at 15%. If, on the other hand, you hold your shares for less than a year, you pay normal income tax, which can go up to 35%. If your shares are worth $1 million, this is the difference between $150,000 and $350,000 in income tax, which is huge.

I'm not going to get into the nuances of this subject, as it's quite complicated. [Read](http://www.quora.com/What-are-the-tax-implications-of-joining-a-startup-as-an-equity-partner) [these](http://www.startupcompanylawyer.com/2008/02/15/what-is-an-83b-election/) [posts](http://www.quora.com/Startups/If-youre-in-a-startup-is-it-ever-a-good-idea-to-exercise-your-options-early-Why-or-why-not), and consult a tax advisor. It can make a huge difference. Also, beware of quarterly tax filings.

## Tricks

I thought it'd be neat to include a couple of other fun tidbits. Did you ever wonder how Romney ended up with [$100 million in a tax-protected IRA](http://www.boston.com/news/politics/articles/2012/08/11/mitt_romneys_ira_is_unlikely_centerpiece_of_wealth_and_tax_avoidance/)? Basically, there are some [tricks that you can play](http://blogs.reuters.com/felix-salmon/2012/07/16/did-romney-put-bain-capital-shares-in-his-ira/) that allow you to put very cheap shares of an early stage company into your IRA (at a very low valuation). If that company's valuation then rises, and the shares become liquid, you can cash out, and have a huge chunk of savings grow tax free in an IRA.

Another neat benefit that executives get are interest free loans when they join. Why might they need such a loan? Well, among other things, [to purchase all of the shares that are offered to them](http://scholarship.law.wm.edu/cgi/viewcontent.cgi?article=1344&context=facpubs) at the time that they join. This starts the clock on the one year capital gains threshold, which drastically reduces their tax basis. Typically such loans are only ever re-paid if the shares become liquid, and the executive cashes out. Pretty good deal.

## Further reading

* [AVC: Musings of a VC in NYC](http://avc.com)
* [Feld Thoughts](http://www.feld.com/)
* [Ask the VC](http://www.askthevc.com/)
* [Both Sides of the Table](http://www.bothsidesofthetable.com/)
* [VC Adventure](http://www.sethlevine.com/)
* [Steve Blank](http://steveblank.com/)
* [Wealthfront Blog](http://blog.wealthfront.com)
* [The Holloway Guide to Equity Compensation](https://www.holloway.com/g/equity-compensation)