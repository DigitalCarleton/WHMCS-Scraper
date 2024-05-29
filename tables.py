from bs4 import BeautifulSoup
import selenium.webdriver.remote.webelement as webelement
from bs4.element import Tag

def clientFromTable(table: webelement.WebElement) -> list[dict[str, str]]:
    clients = []
    soup = BeautifulSoup(table.get_attribute("outerHTML"), "html.parser")
    # Get all 'tr' elements in the table:
    rows = soup.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) == 9:
            client = {'id': cells[1].text,
            'firstName': cells[2].text,
            'lastName': cells[3].text,
            'company': cells[4].text,
            'email': cells[5].text,
            'numServices': int(cells[6].text.split(" ")[0]),
            'dateCreated': cells[7].text,
            'status': cells[8].text}
            clients.append(client)
    return clients 

def servicesFromTable(table: Tag) -> list[dict[str, str]]:
    # Get client's services:
    services = []
    rows = table.find_next_siblings('tr')
    for row in rows:
        cells = row.find_all("td")
        if (len(cells) == 9):
            service = {
                'id': cells[1].text,
                'domain': cells[2].text,
                'status': cells[-2].text
            }    
            services.append(service)
    return services

def notesFromTable(table: Tag) -> str:
    notes = ""
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) > 2:
            note = cells[1]
            notes += f"* {note.text}\n"
    return notes[:-1]