import csv
import requests
import time

# CONFIG
API_KEY = ""  
INPUT_CSV = "wallets.csv"            # CSV file must have a column named "wallet"
OUTPUT_CSV = "profitable_wallets.csv"

HEADERS = {"x-api-key": API_KEY}


def get_wallet_pnl(wallet):
    #Get PNL of a wallet through Solana Tracker API
    url = f"https://data.solanatracker.io/pnl/{wallet}?showHistoricPnL=true"
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            data = response.json()
            summary = data.get("summary", {})
            total = summary.get("total")
            totalInvested = summary.get("totalInvested")
            totalWins = summary.get("totalWins")
            avgBuyValue = summary.get("averageBuyAmount")
            #sometimes API doesn't send one of these values, I just ignore that wallet if it does this.
            if total is None or totalInvested is None or totalWins is None or avgBuyValue is None:
                print(" Unknown Error in API response.")
                return None
            try:
                total = float(total)
                totalInvested = float(totalInvested)
                totalWins = int(totalWins)
                avgBuyValue = float(avgBuyValue)
            except ValueError:
                print(f"Wallet {wallet}: Invalid numeric data in API response.")
                return None
            return total, totalInvested, totalWins, avgBuyValue
        else:
            print(f"Wallet {wallet}: HTTP error {response.status_code}")
            return None
    except Exception as e:
        print(f"Wallet {wallet}: Exception occurred: {e}")
        return None


def main():
    profitable_wallets = []
    
    # Read wallet addresses from the CSV
    with open(INPUT_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            wallet = row.get("wallet")
            if not wallet:
                continue
            wallet = wallet.strip()
            result = get_wallet_pnl(wallet)
            if result is None:
                print(f"Skipping wallet {wallet} due to error.")
                continue
            total, totalInvested, totalWins, avgBuyValue = result
            # Calculate ROI
            roi = (total / totalInvested) * 100
            print(f"Wallet: {wallet}, Total PnL: {total:.2f}, Total Invested: {totalInvested:.2f}, ROI: {roi:.2f}%, Wins: {totalWins}, Avg Buy: ${avgBuyValue:.2f}")
            # Check the profitability criteria for a consistantly successful trader:
            # ROI > 0, profit > $1000, totalWins > 100, avgBuyValue > $50
            if roi > 0 and total > 1000 and totalWins > 10 and avgBuyValue > 50:
                profitable_wallets.append({
                    "wallet": wallet,
                    "ROI": f"{roi:.2f}",
                    "total": f"{total:.2f}",
                    "totalInvested": f"{totalInvested:.2f}",
                    "totalWins": totalWins,
                    "avgBuyValue": f"{avgBuyValue:.2f}"
                })
            # limit is 1 per second, I got rate limited at that though.
            time.sleep(3)
    
    print(f"\nFound {len(profitable_wallets)} profitable wallet(s) meeting all criteria.")
    
    # Writes the profitable wallets to the output CSV
    with open(OUTPUT_CSV, "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ["wallet", "ROI", "total", "totalInvested", "totalWins", "avgBuyValue"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for wallet_info in profitable_wallets:
            writer.writerow(wallet_info)
    
    print(f"Profitable wallets saved to {OUTPUT_CSV}")



if __name__ == "__main__":
    main()
