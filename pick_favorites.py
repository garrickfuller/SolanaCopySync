import csv
from math import sqrt
import requests

#CONFIG
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1271493141333016606/Zr8HKtxEBNMxpoFJzqXH2J0pJDqtA-VEpv9TMgpdPRU2D1OLvNipRDJ1RPxwBHuq2ILO"

def compute_score(total, totalInvested, totalWins, avgBuyValue):
    '''
    First is a score out of 3, where 15% ROI, large amount of wins showing time in market, and a buy unit of 0.5 sol (ish) 
    shows an experienced trader to copy trade.
    '''
    
    roi = (total / totalInvested) * 100 
    score = 0
    if roi >= 15:
        score += 1
  
    if totalWins >= 100:
        score += 1
    
    if avgBuyValue >= 100:
        score +=1


    """
    This one computes a mathmatical score for the wallet.
      - The score is a weighted sum: 50% ROI and 10 times the square root of totalWins.
      - A bonus of +2 is added if the average buy value is at least 200.
    
    The use the square root of totalWins is to reduce the impact of very high win counts
    """
 
    math_score = (0.5 * roi) + (10 * sqrt(totalWins))
    if avgBuyValue >= 200:
        math_score += 20
    return score, math_score, roi
   




    
    




    

def send_to_discord(webhook_url, message):
    """
    Sends the given message to the specified Discord webhook.
    """
    data = {"content": message}
    try:
        response = requests.post(webhook_url, json=data, timeout=10)
        if response.status_code in [200, 204]:
            print("Sent Successfully")
        else:
            print(f"Failed to send message to Discord. Status code: {response.status_code}")
    except Exception as e:
        print(f"Exception when sending message to Discord: {e}")

def main():
    wallets = []
    
    # Read profitable wallets from the CSV
    with open("profitable_wallets.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                total = float(row.get("total", 0))
                totalInvested = float(row.get("totalInvested", 0))
                totalWins = int(row.get("totalWins", 0))
                avgBuyValue = float(row.get("avgBuyValue", 0))
            except ValueError:
                print(f"Skipping row with invalid data: {row}")
                continue
            
            score, math_score, roi = compute_score(total, totalInvested, totalWins, avgBuyValue)
            row["score"] = score           # 3/3 arbitrary score
            row["math_score"] = math_score # Mathematical score
            row["roi_calculated"] = roi
            wallets.append(row)
    
    if not wallets:
        print("No wallets found in the input CSV.")
        return

    # Write all wallets (with computed scores) to favorite_wallets.csv
    fieldnames = list(wallets[0].keys())
    with open("favorite_wallets.csv", "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for wallet in wallets:
            writer.writerow(wallet)
    
    print("Favorite wallets saved to favorite_wallets.csv")
    
    # Build the message for Discord

    # Section 1: List only wallets with a perfect 3/3 score
    message = "**3/3 Scores for Perfect Wallets:**\n"
    perfect_wallets = [wallet for wallet in wallets if wallet["score"] == 3]
    for wallet in perfect_wallets:
        wallet_address = wallet.get("wallet", "N/A")
    message += f"Wallet: `{wallet_address}`, 3/3 Score: `{wallet['score']}`\n"


    
    # Section 2: List top 5 wallets by mathematical score
    top_5_math = sorted(wallets, key=lambda x: x["math_score"], reverse=True)[:5]
    message += "\n**Top 5 Wallets by Mathematical Score:**\n"
    for wallet in top_5_math:
        wallet_address = wallet.get("wallet", "N/A")
        message += (
            f"Wallet: `{wallet_address}`, "
            f"Math Score: `{wallet['math_score']:.2f}`, "
            f"ROI: `{wallet['roi_calculated']:.2f}%`\n"
        )
    
    # Send the summary message to Discord via the webhook
    send_to_discord(DISCORD_WEBHOOK_URL, message)

if __name__ == "__main__":
    main()