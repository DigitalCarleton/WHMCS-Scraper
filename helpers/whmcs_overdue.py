import time

def getOverdueClients(clients: dict[str, str]):
    overdue = []
    senior_year = getSeniorYear()
    for client in clients:
        if 'Students' in client['group']:
            year = client['group'][-4:]
            if int(year) < senior_year:
                overdue.append(client)
        elif "Students" in client['admin_notes']:
            year = client['admin_notes'][-4:]
            if int(year) < senior_year:
                overdue.append(client)
    return overdue

def getSeniors(clients: dict[str, str]):
    seniors = []
    senior_year = getSeniorYear()
    for client in clients:
        if 'Students' in client['group']:
            year = client['group'][-4:]
            if int(year) == senior_year:
                seniors.append(client)
        elif "Students" in client['admin_notes']:
            year = client['admin_notes'][-4:]
            if int(year) == senior_year:
                seniors.append(client)
    return seniors

def getSeniorYear():
    date = time.localtime()
    if date.tm_mon < 7:
        year = date.tm_year
    else: 
        year = date.tm_year + 1
    return year
