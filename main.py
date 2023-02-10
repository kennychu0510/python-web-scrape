from bs4 import BeautifulSoup
from urllib.request import urlopen
from icalendar import Calendar, Event, vCalAddress, vText
import pytz
from datetime import datetime
import os
from pathlib import Path

TEAM = 'KCC'
DIV = '3'
url = "https://www.hksquash.org.hk/public/leagues/results_schedules/id/D00339/league/Squash/year/2022-2023/pages_id/25.html"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

cal = Calendar()

print(pytz.all_timezones)



SCHEDULE = []
# print(soup.get_text())
scheduleTables = soup.find_all('div', {"class": "results-schedules-container"})
count = 0

def makeEvent(date, venue, opponent):
  day = int(date[0])
  month = int(date[1])
  year = int(date[2])
  event = Event()
  event.add('summary', 'HK Squash League - Div ' + DIV + ' vs ' + opponent)
  event.add('dtstart', datetime(year, month, day, 19, 0, 0, tzinfo=pytz.timezone('Hongkong')))
  event.add('dtend', datetime(year, month, day, 22, 0, 0, tzinfo=pytz.timezone('Hongkong')))

  event['organizer'] = 'HK Squash'
  event['location'] = vText(venue)

  # Adding events to calendar
  cal.add_component(event)

for schedule in scheduleTables:
    titleDiv = schedule.find('div', {'class': 'results-schedules-title'})
    # print(titleDiv.findChildren()[0].getText())
    # print(schedule.prettify())
    headers = schedule.find('div', {'class': 'clearfix results-schedules-list'})
    row = schedule.find_all('div', {'class': 'clearfix results-schedules-list'})
    # print(len(row))
    for match in row:
        if (match.find(lambda content: TEAM in content.text)): 
          teamA = match.findChildren()[0].getText() 
          teamB = match.findChildren()[2].getText()
          venue = match.findChildren()[3].getText()
          if (venue == ''):
            venue = 'N/A'
          opponent = teamA
          if (TEAM in teamA):
            opponent = teamB
          matchSchedule = {
            "date": titleDiv.findChildren()[0].getText(),
            "opponent": opponent,
            "venue": venue
          }
          date = matchSchedule['date'].split(' - ')[1].split('/')
        
          makeEvent(date, matchSchedule['venue'], matchSchedule['opponent'])




directory = str(Path(__file__).parent) + "/"
print("ics file will be generated at ", directory)
f = open(os.path.join(directory, 'leagueSchedule.ics'), 'wb')
f.write(cal.to_ical())
f.close()