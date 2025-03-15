from urllib.parse import urlparse, parse_qs

url = 'http://114.35.229.141/_handler/Match.ashx?CupID=20&MatchID=1&SetNum=0'

def get_cupid(url):
    parse_url = urlparse(url)

    #Get the elements after ? in URL
    urlelement = parse_qs(parse_url.query)

    #Get the cupid from the URL
    cupid = urlelement.get('CupID')

    if cupid:
        return int(cupid[0])
    else:
        ("N/A")

cup = get_cupid(url)
print(cup)