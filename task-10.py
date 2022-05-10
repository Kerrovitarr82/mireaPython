def delete_empty_rows(table):
    table = [row for row in table if row[0] is not None]
    return table


def delete_duplicate_columns(table):
    for row in table:
        del row[2]
    return table


def delete_duplicate_rows(table):
    setBuff = set()
    newTable = []
    for itemBuff in table:
        t = tuple(itemBuff)
        if t not in setBuff:
            newTable.append(itemBuff)
            setBuff.add(t)
    return newTable


def split_column(table):
    for itemBuff in table:
        strBuff = itemBuff[1]
        strBuff = strBuff.split("|")
        str1 = strBuff[0][6:]
        str2 = strBuff[0][0:2]
        strBuff[0] = str1 + strBuff[0][2:6] + str2
        itemBuff[1] = strBuff[0]
        sep = strBuff[1].find("[")
        itemBuff.append(strBuff[1][0:sep])
    return table


def name_change(table):
    for itemBuff in table:
        strBuff = itemBuff[0]
        sep = strBuff.find(" ")
        strName = strBuff[sep + 1:sep + 3]
        strBuff = strName + " " + strBuff[0:sep - 1]
        itemBuff[0] = strBuff
    return table


def round_numbers(table):
    for itemBuff in table:
        strBuff = float(itemBuff[2]).__round__(1)
        itemBuff[2] = str(strBuff)
    return table


def main(table):
    table = delete_empty_rows(table)
    table = delete_duplicate_columns(table)
    table = delete_duplicate_rows(table)
    table = split_column(table)
    table = name_change(table)
    table = round_numbers(table)
    table.sort(key=lambda row: (row[3]))
    return table


table1 = [["Тавешов, С.И.", "04.04.24|tavesov27[at]rambler.ru", "0.39", "0.39"],
          ["Цоразев, Л.М.", "03.11.25|zorazev67[at]gmail.com", "0.78", "0.78"],
          [None, None, None, None],
          ["Ротадянц, А.С.", "04.01.02|rotadanz89[at]yahoo.com", "0.97", "0.97"],
          ["Цоразев, Л.М.", "03.11.25|zorazev67[at]gmail.com", "0.78", "0.78"],
          [None, None, None, None],
          ["Вилий, П.К.", "03.01.23|vilij95[at]mail.ru", "0.12", "0.12"]]

for item in main(table1):
    print(item)
