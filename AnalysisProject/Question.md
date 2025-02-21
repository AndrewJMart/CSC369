# Proposal: Analysis of Major Game Titles' Review Trends Over Time

## 1. What Question Are You Trying to Answer?

Have major game titles from large, common AAA developers decreased in reviews/ratings over the last years compared to a long time ago? (And if applicable, for these large lackluster titles investigate if there truly are commonalities shared between them.)

## 2. Why Is This Question Worth Answering?

The gaming industry has seen massive shifts in development strategies, monetization models, and player expectations. Understanding whether AAA game reviews have declined over time can provide insights into the industry's health, the impact of microtransactions, rushed releases, and shifting consumer sentiment.

This question is relevant because many gamers and industry analysts have debated whether AAA titles have declined in quality and reception. For example, major releases like *Cyberpunk 2077* and *Battlefield 2042* received significant backlash at launch, leading to negative reviews and controversy.

## 3. What Is Your Hypothesis? What Leads You Towards That Hypothesis?

**Hypothesis:** AAA game reviews have trended downward over time, with modern titles receiving lower ratings compared to older releases.

This hypothesis is based on several observed trends:
- An increase in microtransactions, live-service models, and rushed development cycles.
- Numerous high-profile releases suffering from performance issues and incomplete content at launch.
- A shift in review culture, where consumers are more critical and vocal about industry practices.

## 4. What Is the Primary Dataset You Will Use to Answer the Question?

**Dataset:** 113,883,717 Steam user reviews

This dataset contains the following relevant information:
- Steam user ID, number of games owned, number of reviews written.
- Playtime statistics (all-time, last 2 weeks, at time of review, last played).
- Review metadata: language, creation time, update time.
- Sentiment: whether the review was positive or negative.
- Engagement metrics: number of upvotes, funny votes, helpfulness score, number of comments.
- Purchase details: whether the game was bought on Steam or obtained for free.
- Early Access indicator: whether the review was written during the game's Early Access phase.
- Developer response and response timing (if applicable).
- Game Title: Provides information on what game was actually reviewed (essential for project)

**Dataset Source:** [Steam Reviews Dataset](https://www.kaggle.com/datasets/kieranpoc/steam-reviews/data)

