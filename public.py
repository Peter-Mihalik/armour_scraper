from typing import List

def getLinksFromATags(a_tags:List[str]) -> List[str]:
    links = []
    for a_tag in a_tags:
        links.append(a_tag['href'])
    return links


def getSrcFromImgs(imgs:List) -> List[str]:
    srces = []
    for img in imgs:
        src = img['src']
        srces.append(src)

    return srces