import re


def main(source):
    source = source.replace("{", "")
    source = source.replace("}", "")
    source = source.replace("<<", "")
    source = source.replace(">>", "")
    source = source.replace("make", "")
    p = r"[-+]?\w+"
    matches = re.findall(pattern=p, string=source)
    response = {}
    for i in range(len(matches)):
        j = i + 1
        arr = []
        if re.match(r"[-+]?\d+", matches[i]) is not None:
            continue
        while j < len(matches) and re.match(r"[-+]?\d+", matches[j]) is not None:
            arr.append(int(matches[j]))
            j += 1
        response[matches[i]] = arr
    return response


print(main("{ <<make bece_692 :{ -1623 -1202 }>>, << make erzaat_509 :{7029 1646-841 } >>, "
           "<<make onus: { -3357 -9883 -5039}>>, }"))
