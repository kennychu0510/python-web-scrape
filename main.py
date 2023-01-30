from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "https://www.hksquash.org.hk/public/leagues/results_schedules/id/D00339/league/Squash/year/2022-2023/pages_id/25.html"

page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

SCHEDULE = []
# print(soup.get_text())
scheduleTables = soup.find_all('div', {"class": "results-schedules-container"})
count = 0
for schedule in scheduleTables[2:]:
    titleDiv = schedule.find('div', {'class': 'results-schedules-title'})
    # print(titleDiv.findChildren()[0].getText())
    # print(schedule.prettify())
    headers = schedule.find('div', {'class': 'clearfix results-schedules-list'})
    row = schedule.find_all('div', {'class': 'clearfix results-schedules-list'})
    # print(len(row))
    for match in row:
        if (match.find(lambda content: "KCC" in content.text)): 
          teamA = match.findChildren()[0].getText() 
          teamB = match.findChildren()[2].getText()
          venue = match.findChildren()[3].getText()
          if (venue == ''):
            venue = 'N/A'
          opponent = teamA
          if ("KCC" in teamA):
            opponent = teamB
          matchSchedule = {
            "date": titleDiv.findChildren()[0].getText(),
            "opponent": opponent,
            "venue": venue
          }
          print(matchSchedule)
          print('\n')
    # break
