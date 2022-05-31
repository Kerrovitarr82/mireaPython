import re


def main(source):
    source = source.replace("||", "")
    source = source.replace("<block>", "")
    source = source.replace("</block>", "")
    source = source.replace("glob", "")
    source = source.replace("#", "")
    source = source.replace(".", "")
    p = r"[-+]?\w+"
    matches = re.findall(pattern=p, string=source)
    response = {}
    matches.reverse()
    for i in range(len(matches)):
        arr = []
        if re.match(r"[-+]?\d+", matches[i]) is None:
            j = i + 1
            while j < len(matches) and re.match(r"[-+]?\d+",
                                                matches[j]) is not None:
                arr.append(int(matches[j]))
                j += 1
            arr.reverse()
            response[matches[i]] = arr
    return dict(reversed(list(response.items())))


print(main("||<block> glob #( #8725 . #-2545 . #-5257 . #-4627) ->isgeza. </block>; <block> glob #( #9207 .#-5364 . "
           "#9220 .#-5091 ) -> ated.</block>; <block>glob #( #5344 . #7114 .#-1678 .#5089)-> dila.</block>; <block> "
           "glob #( #-5420 . #-9376 )-> zala_15. </block>; ||"))
