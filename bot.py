#### COVID-19 SINGAPORE -- TELEGRAM BOT WITH COVID-19 UPDATES FROM SINGAPORE
# Reports the latest COVID-19 statistics from Singapore.
# Created by: Stanley Tan (https://github.com/stanley-1)
# Code snippets for hosting Telegram bots on Heroku adapted from: Liu Haohui (https://github.com/liuhh02/python-telegram-bot-heroku)


import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import requests
from bs4 import BeautifulSoup
PORT = int(os.environ.get('PORT', '8443'))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = 'REDACTED'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    message = "Welcome to COVID-19 Updates from Singapore!" + "\n\nYou can control me by using the following commands:\n\n"
    message += "/newcases - latest daily caseload\n"
    message += "/pastmonth - COVID-19 statistics from the past month\n"
    message += "/bor - bed occupancy & ICU numbers\n"
    message += "/vax - vaccination progress\n"
    message += "/total - cumulative cases & deaths\n"
    message += "/all - comprehensive summary of all COVID-19 related data\n"
    update.message.reply_text(message)

def help(update, context):
    """Send a message when the command /help is issued."""
    message = "You can control me by using the following commands:\n\n"
    message += "/newcases - latest daily caseload\n"
    message += "/pastmonth - COVID-19 statistics from the past month\n"
    message += "/bor - bed occupancy & ICU numbers\n"
    message += "/vax - vaccination progress\n"
    message += "/total - cumulative cases & deaths\n"
    message += "/all - comprehensive summary of all COVID-19 related data\n"
    update.message.reply_text(message)

def newCases(update, context):
    # Create url
    url = 'https://www.moh.gov.sg/'
    # Define headers
    headers = { 'User-Agent': 'Generic user agent' }
    # Get page
    page = requests.get(url, headers=headers)
    # Soup the page
    soup = BeautifulSoup(page.text, 'html.parser')

    # More specific info
    try:
        # Get Statistics
        dailyCases = soup.find('div', {'id':'ContentPlaceHolder_contentPlaceholder_C088_Col00'}).text
        sortedStats = dailyCases.rstrip().split("As of")
        
        #*** New Cases ***#
        newCases = sortedStats[2]
        newCases = newCases.split('\n')
        try:
            while True:
                newCases.remove('')
        except ValueError:
            pass

        #** Making Sense of Numbers **#
        date = "\nDaily Caseload\nAs of" + newCases[0]
        localPCR = newCases[2]
        localART = newCases[4]
        localTotal = int(localPCR.replace(",", "")) + int(localART.replace(",", ""))

        importPCR = newCases[6].split("Imported")[0]
        importART = newCases[7]
        importTotal = int(importPCR.replace(",", "")) + int(importART.replace(",", ""))

        totalNew = localTotal + importTotal

        discharged = newCases[9]
        deaths = newCases[11]
        ratio = newCases[13]
        
        newCasesStatement = date + "\nLocal PCR: " + localPCR + "\nLocal ART: " + localART + "\nTotal New Local Cases: " + str(localTotal) + "\n"
        newCasesStatement += "\nImported PCR: " + importPCR + "\nImported ART: " + importART + "\nTotal New Imported Cases: " + str(importTotal) + "\n"
        newCasesStatement += "\nTotal New Cases: " + str(totalNew) + "\n"
        newCasesStatement += "\nDischarged: " + discharged + "\nDeaths: " + deaths + "\nWeek on Week Infection Ratio: " + ratio
        update.message.reply_text(newCasesStatement)
        
    except:
        update.message.reply_text('Something went wrong...')


def pastMonth(update, context):
    # Create url
    url = 'https://www.moh.gov.sg/'
    # Define headers
    headers = { 'User-Agent': 'Generic user agent' }
    # Get page
    page = requests.get(url, headers=headers)
    # Soup the page
    soup = BeautifulSoup(page.text, 'html.parser')

    # More specific info
    try:
        # Get Statistics
        dailyCases = soup.find('div', {'id':'ContentPlaceHolder_contentPlaceholder_C088_Col00'}).text
        sortedStats = dailyCases.rstrip().split("As of")
        
        #*** Past Cases ***#
        pastCases = sortedStats[2]
        pastCases = pastCases.split('\n')
        try:
            while True:
                pastCases.remove('')
        except ValueError:
            pass

        #** Making Sense of Numbers **#
        date = "\n" + pastCases[16]
        infected = pastCases[18]
        noMild = pastCases[19]
        o2supp = pastCases[21]
        icu = pastCases[23]
        died = pastCases[25]

        
        pastCasesStatement = date + "\nInfected: " + infected + "\nHad No or Mild Symptoms: " + noMild + "\nRequired Oxygen Supplementation: "
        pastCasesStatement += o2supp + "\nICU: " + icu + "\nDied: " + died
        update.message.reply_text(pastCasesStatement)
        
    except:
        update.message.reply_text('Something went wrong...')


def bor(update, context):
    # Create url
    url = 'https://www.moh.gov.sg/'
    # Define headers
    headers = { 'User-Agent': 'Generic user agent' }
    # Get page
    page = requests.get(url, headers=headers)
    # Soup the page
    soup = BeautifulSoup(page.text, 'html.parser')

    # More specific info
    try:
        # Get Statistics
        dailyCases = soup.find('div', {'id':'ContentPlaceHolder_contentPlaceholder_C088_Col00'}).text
        sortedStats = dailyCases.rstrip().split("As of")
        
        #*** Bed Occupancy ***#
        bedOccupancy = sortedStats[1]
        bedOccupancy = bedOccupancy.split('\n')
        try:
            while True:
                bedOccupancy.remove('')
        except ValueError:
            pass

        #** Making Sense of Numbers **#
        date = "\nBed Occupancy Statistics\nAs of" + bedOccupancy[0]
        hospitalised = bedOccupancy[2]
        o2supp = bedOccupancy[3]
        icu = bedOccupancy[5]
        bedOccupancyStatement = date + "\nHospitalised: " + hospitalised + "\nOn Oxygen Supplementation: " + o2supp + "\nICU: " + icu
        update.message.reply_text(bedOccupancyStatement)
        
    except:
        update.message.reply_text('Something went wrong...')


def vaxRate(update, context):
    # Create url
    url = 'https://www.moh.gov.sg/'
    # Define headers
    headers = { 'User-Agent': 'Generic user agent' }
    # Get page
    page = requests.get(url, headers=headers)
    # Soup the page
    soup = BeautifulSoup(page.text, 'html.parser')

    # More specific info
    try:
        # Get Statistics
        dailyCases = soup.find('div', {'id':'ContentPlaceHolder_contentPlaceholder_C088_Col00'}).text
        sortedStats = dailyCases.rstrip().split("As of")
        
        #*** Vaccination Progress ***#
        vaxRate = sortedStats[3]
        vaxRate = vaxRate.split('\n')
        try:
            while True:
                vaxRate.remove('')
        except ValueError:
            pass

        #** Making Sense of Numbers **#
        date = "\nVaccination Progress\nAs of" + vaxRate[0]
        oneDose = vaxRate[1]
        complete = vaxRate[3].split("population")[0] + "population"
        complete2 = vaxRate[3].split("population")[1] + "population"
        booster = vaxRate[5]
        vaxRateStatement = date + "\nReceived at least 1 dose: " + oneDose + "\nCompleted full regimen: " + complete + " & " + complete2
        vaxRateStatement += "\nReceived booster shots: " + booster
        update.message.reply_text(vaxRateStatement)        
        
    except:
        update.message.reply_text('Something went wrong...')


def total(update, context):
    # Create url
    url = 'https://www.moh.gov.sg/'
    # Define headers
    headers = { 'User-Agent': 'Generic user agent' }
    # Get page
    page = requests.get(url, headers=headers)
    # Soup the page
    soup = BeautifulSoup(page.text, 'html.parser')

    # More specific info
    try:
        # Get Statistics
        dailyCases = soup.find('div', {'id':'ContentPlaceHolder_contentPlaceholder_C088_Col00'}).text
        sortedStats = dailyCases.rstrip().split("As of")
        
        #*** Cumulative Cases & Deaths ***#
        cumCases = sortedStats[4]
        cumCases = cumCases.split('\n')
        try:
            while True:
                cumCases.remove('')
        except ValueError:
            pass

        #** Making Sense of Numbers **#
        date = "\nCumulative Statistics\nAs of" + cumCases[0]
        cases = cumCases[2]
        deaths = cumCases[3]
        cumCasesStatement = date + "\nTotal Cases: " + cases + "\nTotal Deaths: " + deaths
        update.message.reply_text(cumCasesStatement)        
        
    except:
        update.message.reply_text('Something went wrong...')


def all(update, context):
    # Create url
    url = 'https://www.moh.gov.sg/'
    # Define headers
    headers = { 'User-Agent': 'Generic user agent' }
    # Get page
    page = requests.get(url, headers=headers)
    # Soup the page
    soup = BeautifulSoup(page.text, 'html.parser')

    # More specific info
    try:
        # Get Statistics
        dailyCases = soup.find('div', {'id':'ContentPlaceHolder_contentPlaceholder_C088_Col00'}).text
        sortedStats = dailyCases.rstrip().split("As of")
        
        bedOccupancy = sortedStats[1]
        newCases = sortedStats[2]
        pastCases = sortedStats[2]
        vaxRate = sortedStats[3]
        cumCases = sortedStats[4]
        
        #*** Bed Occupancy ***#
        bedOccupancy = bedOccupancy.split('\n')
        try:
            while True:
                bedOccupancy.remove('')
        except ValueError:
            pass

        #** Making Sense of Numbers **#
        date = "\nBed Occupancy Statistics\nAs of" + bedOccupancy[0]
        hospitalised = bedOccupancy[2]
        o2supp = bedOccupancy[3]
        icu = bedOccupancy[5]
        bedOccupancyStatement = date + "\nHospitalised: " + hospitalised + "\nOn Oxygen Supplementation: " + o2supp + "\nICU: " + icu
        update.message.reply_text(bedOccupancyStatement)

        #*** New Cases ***#
        newCases = newCases.split('\n')
        try:
            while True:
                newCases.remove('')
        except ValueError:
            pass
        # print(newCases)

        #** Making Sense of Numbers **#
        date = "\nDaily Caseload\nAs of" + newCases[0]
        localPCR = newCases[2]
        localART = newCases[4]
        localTotal = int(localPCR.replace(",", "")) + int(localART.replace(",", ""))

        importPCR = newCases[6].split("Imported")[0]
        importART = newCases[7]
        importTotal = int(importPCR.replace(",", "")) + int(importART.replace(",", ""))

        totalNew = localTotal + importTotal

        discharged = newCases[9]
        deaths = newCases[11]
        ratio = newCases[13]
        
        newCasesStatement = date + "\nLocal PCR: " + localPCR + "\nLocal ART: " + localART + "\nTotal New Local Cases: " + str(localTotal) + "\n"
        newCasesStatement += "\nImported PCR: " + importPCR + "\nImported ART: " + importART + "\nTotal New Imported Cases: " + str(importTotal) + "\n"
        newCasesStatement += "\nTotal New Cases: " + str(totalNew) + "\n"
        newCasesStatement += "\nDischarged: " + discharged + "\nDeaths: " + deaths + "\nWeek on Week Infection Ratio: " + ratio
        update.message.reply_text(newCasesStatement)

        #*** Past Cases ***#
        pastCases = pastCases.split('\n')
        try:
            while True:
                pastCases.remove('')
        except ValueError:
            pass

        #** Making Sense of Numbers **#
        date = "\n" + pastCases[16]
        infected = pastCases[18]
        noMild = pastCases[19]
        o2supp = pastCases[21]
        icu = pastCases[23]
        died = pastCases[25]

        
        pastCasesStatement = date + "\nInfected: " + infected + "\nHad No or Mild Symptoms: " + noMild + "\nRequired Oxygen Supplementation: "
        pastCasesStatement += o2supp + "\nICU: " + icu + "\nDied: " + died
        update.message.reply_text(pastCasesStatement)

        #*** Vaccination Progress ***#
        vaxRate = vaxRate.split('\n')
        try:
            while True:
                vaxRate.remove('')
        except ValueError:
            pass

        #** Making Sense of Numbers **#
        date = "\nVaccination Progress\nAs of" + vaxRate[0]
        oneDose = vaxRate[1]
        complete = vaxRate[3].split("population")[0] + "population"
        complete2 = vaxRate[3].split("population")[1] + "population"
        booster = vaxRate[5]
        vaxRateStatement = date + "\nReceived at least 1 dose: " + oneDose + "\nCompleted full regimen: " + complete + " & " + complete2
        vaxRateStatement += "\nReceived booster shots: " + booster
        update.message.reply_text(vaxRateStatement)
        

        #*** Cumulative Cases & Deaths ***#
        cumCases = cumCases.split('\n')
        try:
            while True:
                cumCases.remove('')
        except ValueError:
            pass

        #** Making Sense of Numbers **#
        date = "\nCumulative Statistics\nAs of" + cumCases[0]
        cases = cumCases[2]
        deaths = cumCases[3]
        cumCasesStatement = date + "\nTotal Cases: " + cases + "\nTotal Deaths: " + deaths
        update.message.reply_text(cumCasesStatement)        
        
    except:
        update.message.reply_text('Something went wrong...')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("newcases", newCases))
    dp.add_handler(CommandHandler("pastmonth", pastMonth))
    dp.add_handler(CommandHandler("bor", bor))
    dp.add_handler(CommandHandler("vax", vaxRate))
    dp.add_handler(CommandHandler("total", total))
    dp.add_handler(CommandHandler("all", all))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN,
        webhook_url='https://REDACTED.herokuapp.com/' + TOKEN
    )

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
