---
title: "[Notes] Why Data Scientists and Data Engineers Need Sales Skills"
description: "Thoughts after reading how the CEO of Terminal X built a sales team. Engineers and data scientists need the kind of selling that starts from the other person's point of view, and unlike in sales, experience at real scale matters a lot in these jobs. If you don't have it yet, build as much end to end as you can."
pubDatetime: 2026-10-25T22:00:00Z
koSlug: sales-skills-for-data-people
tags:
  - career
  - machine-learning
---

A while ago I read a short post by the CEO of Terminal X about how he put together a sales team. Many Korean retail investors know him as the YouTuber 뉴욕주민 ("New York resident"). Terminal X is a financial AI start-up that helps investment managers connect their internal data and ways of working to AI and use it in day-to-day investing.

As I understood it, when he hired salespeople, how big an organisation they had sold for didn't count for much. A start-up's product is new and hardly anyone knows the name, so experience selling with a big company's brand behind you doesn't carry over. So in interviews he asked candidates to "sell me this", and looked for people who could sell it better than the people who built it, or make even the builders want to buy it.

It sounds obvious, yet I kept coming back to it.

## Everyone at work is selling something

Back when I was a student I read a book that said anyone with a job needs basic sales skills. I can't recall the title; I think it was one of those books about wealth and success full of stories about Carnegie. At the time I just nodded along, but the longer I work, the more often it comes back to me.

Daniel Pink made a similar case in *To Sell Is Human*. About one in nine American workers sells for a living, but he cites survey results suggesting the rest also spend around 40% of their working time persuading other people. He calls this "non-sales selling", where what you ask people to give up is their time, attention or effort rather than money. ([Wharton](https://knowledge.wharton.upenn.edu/article/daniel-pink-on-why-to-sell-is-human/))

## Engineers and data scientists too

I think this skill matters a lot for engineers and data scientists as well. A well-built model only counts once the business uses it, and an analysis only changes something once the person making the decision accepts it. A model that is a few points better still won't make it into production if the people who would use it can't see why they should switch.

The selling I mean here has less to do with being a smooth talker and more to do with thinking from the other person's side. You have to start from what the user needs and where they get stuck, and plenty of the engineers I have worked with were strong technically but weak at exactly this. They build what they want to build first and look for someone to use it afterwards. The steady growth of customer-facing roles such as [forward deployed engineers](/en/fde-forward-deployed-engineer/) looks to me like an attempt to close that gap.

Translated into an engineering interview, "sell me this" might become "sell the model you built last quarter to the person in the business who is meant to use it". I suspect it would be fairly easy to tell apart the candidates who list technical details from the ones who start with how that person's daily work would change.

## Scale still matters

Unlike in sales, though, I think the kind of team and the scale you worked at do make a real difference for data scientists and engineers. If you were a cog turning the same handle at a large company, that counts for little. But having dealt first hand with the problems that come with heavy traffic and serving a large user base is hard to get anywhere else.

Serving a model on one GPU and scaling out to twenty to keep up with demand are very different jobs. How to spread requests, what happens when one machine dies, how to roll out a new model gradually and roll it back when something breaks, where the cost is leaking: these problems only show up once you are at scale. The same goes for data. Once a dataset outgrows a laptop's memory and moves to distributed processing, even a single join or deduplication has to be written differently. That most production failures start [outside the model](/en/ai-system-fails-outside-model/) is also something you only really absorb after living through a few of them.

## If you haven't worked at that scale

On the other hand, if you have never handled heavy traffic, you are probably in a good position to get end-to-end experience. In a small team one person often owns everything from data collection through modelling, serving and monitoring. At a big company you can spend years on one slice of that, so having built the whole flow yourself is a real advantage.

What seems realistic to me is to build things end to end as far as you can, and fill in the scaling side separately by reading up on where it would break first. Big tech engineering blogs, conference talks and YouTube have plenty of write-ups on problems hit while scaling up. It isn't the same as going through it yourself, but it shortens the learning curve a lot.

Thinking from the other side and persuading people is needed in any role, and for data people, experience at scale on top of that makes them much more solid. If you don't have that experience yet, build something small all the way through and learn the scaling problems in advance from what others have written down. That's just my take.

---

**Related posts:**

- [Thinking About the FDE: Ten Names, One Job](/en/fde-forward-deployed-engineer/)
- [The Model Is Smart, So Why Is the System Stupid? Most AI Failures Start Outside the Model](/en/ai-system-fails-outside-model/)

## References

- [Terminal X partners with OpenAI and starts its Asia push in Japan (Hankyung, 2026-08-27, in Korean)](https://www.hankyung.com/article/202608276874i)
- [Daniel Pink on Why 'To Sell Is Human' (Knowledge at Wharton)](https://knowledge.wharton.upenn.edu/article/daniel-pink-on-why-to-sell-is-human/)
- [Dan Pink: Like It or Not, You're Probably a Salesperson (Big Think)](https://bigthink.com/?p=54168)
