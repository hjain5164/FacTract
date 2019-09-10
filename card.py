from bs4 import BeautifulSoup
import wikipedia


def make_card(user_input):
    try:
        pg = wikipedia.WikipediaPage(title=user_input)
    except:
        p = wikipedia.search(query=user_input, suggestion=True)
        user_input = p[0][0]
        pg = wikipedia.WikipediaPage(title=user_input)

    pghtml = pg.html()

    soup = BeautifulSoup(pghtml, 'html.parser')
    table = soup.table
    heads = table.findAll('tr')
    info_box = []
    for head in heads[:7]:
        info_box.append(head.get_text())
    # print info_box
    # non reg ex way of dealing with expressions

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

    if len(info_box) > 2:
        for x in range(7):
            print '-----------------------'
            print info_box[x]
            info_box[x] = removeNestedParentheses(info_box[x])
        return info_box[1:]
    else:
        return " "
