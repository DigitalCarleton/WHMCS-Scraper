# Writing to file:
def writeFile(filename: str, clients: list[dict[str, str]]):
    f = open(filename, "w")
    # Headers:
    keys = ["id", "firstName", "lastName", "email", "status", "group", "adminNotes", "numServices", "services", "notes"]
    f.write(",".join(keys) + "\n")
    # Body:
    for client in clients:
        if 'services' in client:
            client['services'] = translateServices(client['services'])
        line = []
        for key in keys:
            if key in client:
                line.append(str(client[key]))
            else:
                line.append("")
        f.write(",".join(line) + "\n")
    f.close()

# Translate our services into a string for the cells in the CSV file
def translateServices(services: list[dict[str, str]]) -> str:
    s = []
    for service in services:
        s.append(f"{service['id']} | {service['domain']} | {service['status']}")
    return "\\n".join(s)