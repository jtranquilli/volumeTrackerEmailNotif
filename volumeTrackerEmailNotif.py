import yfinance as fy
import pandas as pd
import smtplib
import time

sender_email = "redacted"
rec_email = "redacted"
password = "redacted"
message = ""
m = ""

df = pd.read_csv('/Users/juliustranquilli/desktop/companylist.csv')

print(df['Symbol'])

upSymbols = []

for stock in df['Symbol']:
    stock = stock.upper()
    if '^' in stock: #ignoring formatting problems in the .csv file
        pass
    
    else:
        try:
            time.sleep(0.25)
            
            stock_info = fy.Ticker(stock)

            history = stock_info.history(period="5d")

            prevAverageVol = history['Volume'].iloc[1:4:1].mean()
            #third value in iloc call is just increment of 1

            today_vol = history['Volume'][-1]

            if (today_vol > prevAverageVol * 3) :

                upSymbols.append(stock)
                
        except:
            pass


for i in range(len(upSymbols)):
    message += upSymbols[i]
    message += " , "
    
    
print(upSymbols)

server = smtplib.SMTP('smtp.gmail.com', 587)

server.starttls()

server.login(sender_email, password)

print("Login success")
server.sendmail(sender_email, rec_email, message)
print("Email has been sent to", rec_email)
