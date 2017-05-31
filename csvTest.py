import csv


def addNewLine(file):
    with open(file, "r+") as f:
        f.seek(0, 2)
        if(f.read() != '\n'):
            f.seek(0, 2)
            f.write('\n')

fields = ['2311223/liquid-vs-optic-esl-pro-league-season-5-finals', '2311224/nrg-vs-north-esl-pro-league-season-5-finals', '2311221/nrg-vs-optic-esl-pro-league-season-5-finals']
with open(r'csv/name.csv', 'a', encoding='utf-8') as f:
    print(f)
    writer = csv.writer(f, delimiter=',')
    addNewLine("csv/name.csv")
    for i in range(0, len(fields)):
        writer.writerow([fields[i]])
