def incCount(count):
    if count < 9:
        count += 1
        return count, False
    else:
        count = 0
        return count, True

def extractInfo(validLine, count):
    if count != 2:
        info = validLine.split('>')[1].split('<')[0]
    else:
        info = validLine.split('<')[1].split('>')[1].split('<')[0]
    return info


def getData(soup):
    possibleStyles = {0: 'participant', 1: 'participant', 2: 'matchupDate', 3: 'price', 4: 'price', 5: 'price', 6: 'price', 7: 'price', 8: 'price', 9: 'price'}
    count = 0
    theRows = []
    row = []
    divs = soup.find_all('div')
    children = divs[2].findChildren("div", {'class': 'contentBlock square'}, recursive=True)
    for child in children:
        lines = str(child).split()
        for i in range(len(lines)):
            validLine = ''
            if 'style' in lines[i]:
                    if possibleStyles.get(count) in lines[i]:
                        validLine = lines[i]
                        if '<' not in lines[i]:
                            validLine += " " + lines[i+1]
                    if len(validLine) > 0:
                        info = extractInfo(validLine, count)
                        count, checkReset = incCount(count)
                        row.append(info)
                        if checkReset == True:
                            theRows.append(row)
                            row = []

    for row in theRows:
        print(row)

    import csv
    with open('output.csv', 'w') as outcsv:
        writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(['TEAM 1', 'TEAM 2', 'TIME', 'ML 1', 'ML DRAW', 'ML 2', 'SPREAD 1', 'SPREAD 2', 'OVER', 'UNDER'])
        for row in theRows:
            writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])

if __name__ == '__main__':
    from selenium import webdriver
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.firefox.options import Options

    options = Options()
    profile_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    options.binary_location = (profile_path)

    service = Service(r'D:\bsaub\Downloads\geckodriver.exe')
    driver = webdriver.Firefox(service=service, options=options)
    driver.get('https://www.pinnacle.com/en/soccer/england-premier-league/matchups#period:0:moneyline')
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    getData(soup)







