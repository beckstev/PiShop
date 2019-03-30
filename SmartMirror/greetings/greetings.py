from random import choice

def get_compliment():
    '''Chooses a random compliment
    Requirements    compliments.txt file in the same directory
    Output          string containing a compliment'''
    with open('compliments.txt', 'r') as compliment_file:
        compliments = compliment_file.readlines()
    compliments = [comp.strip('\n') for comp in compliments]
    return choice(compliments)


def get_quote():
    '''Chooses a random quote
    Requirements    quotes.txt file in the same directory
    Output          string containing a quote'''
    with open('quotes.txt', 'r') as quote_file:
        quotes = quote_file.readlines()
    quotes = [quote.strip('\n') for quote in quotes]
    return choice(quotes)
