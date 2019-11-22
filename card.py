from bs4 import BeautifulSoup
import wikipedia


def make_card(user_input):
    try:
        pg = wikipedia.WikipediaPage(title=user_input)
    except:
        p = wikipedia.search(query=user_input, suggestion=True)
        user_input = p[0][0]
        pg = wikipedia.WikipediaPage(title=user_input)

    try:
        pghtml = pg.html()
        soup = BeautifulSoup(pghtml, 'html.parser')
        table = soup.table
        # row = table.findAll('tr')
        heading = table.findAll('th')
        data = table.findAll('td')
        # heads = table.findAll('tr')
    except:
        return " "
    info_box = []

    for h, d in zip(heading[:7], data[:7]):
        info_box.append(h.get_text()+':  '+d.get_text())

    # for head in heads[:7]:
        # info_box.append(head.get_text())

    def removeNestedParentheses(s):
        ret = ''
        skip = 0
        for i in s:
            if i == '[':
                skip += 1
            elif i == ']'and skip > 0:
                skip -= 1
            elif skip == 0:
                ret += i
        return ret
    print(len(info_box))
    if len(info_box) > 2:
        for x in range(len(info_box)):
            info_box[x] = removeNestedParentheses(info_box[x])
        return info_box[1:]
    else:
        return " "


print(make_card('Snapdragon'))
