# SolanaCopySync

## Solana CopySnyc is a free way to mass search wallets to find low-key copy trades!

get_transactions.py 
  Uses wallets from wallets.csv, outputs all profitable wallets into profitable_wallets.csv

pick_favorites.py
  Returns the top wallets by score to a discord webhook.

### Disclaimer: Most People really suck at trading Solana memecoins. The free plan has a rate limit so it will take a while to find your unicorn wallets. 
<img width="1112" alt="Screenshot 2025-03-04 at 10 45 07 PM" src="https://github.com/user-attachments/assets/0487f4d5-3ba8-413b-a223-56c7a2d40a5f" />
<img width="1056" alt="Screenshot 2025-03-04 at 11 21 09 PM" src="https://github.com/user-attachments/assets/b9d2f3bb-5d4a-4a92-8906-027b49cdf8fd" />
<img width="927" alt="Screenshot 2025-03-04 at 11 26 37 PM" src="https://github.com/user-attachments/assets/0da62e72-5ec5-4695-8e91-5086957347d4" />

## CONFIG

You need a Solana Tracker API key https://www.solanatracker.io/
Free plan works just fine

have a wallet.csv with wallets to mass scrape. 
here is the easy way to collect a huge list of sol exchange outflow.

Use a chrome extension scraper and go to an exchange account, go to transfers tab on solscan, adjust filters to outflow, sol and 2 sol.
It will list all sol going out of the exchange to wallets all over solana.
Set show 100 or more rows. Get the chrome extension to highlight just the “to” wallets. And scroll through some pages.
You will collect thousands of addresses, save it as a csv and remove duplicates

You can edit the standard score critera on what you want it to judge by changing the values on this code snippet.
```
roi = (total / totalInvested) * 100 
    score = 0
    if roi >= 15:
        score += 1
  
    if totalWins >= 100:
        score += 1
    
    if avgBuyValue >= 100:
        score +=1
```

I suggest copying through https://www.odinbot.io/

