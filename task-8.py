import re


def main(source):
    source = source.replace(".do", "")
    source = source.replace(".end", "")
    source = source.replace("variable", "")
    p = r"[-+]?\w+"
    matches = re.findall(pattern=p, string=source)
    response = {}
    for i in range(len(matches)):
        if re.match(r"[-+]?\d+", matches[i]) is not None:
            continue
        response[matches[i]] = int(matches[i-1])
    return response


print(main(".do <% variable 775 -> `ususus; %>; <% variable 752 ->`isan_379;%>;"
           "<% variable -9498 ->`inar; %>;<% variable -4052 -> `isquor; %>; .end"))
