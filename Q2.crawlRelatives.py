import lxml.html
import requests

max_urls_to_crawl = 50
wiki = "https://en.wikipedia.org"
xpath_exp = [
    "//tr[th='Mother']//@href[contains(.,'wiki')]",
    "//tr[th='Father']//@href[contains(.,'wiki')]",
    "//tr[th='Spouse']//@href[contains(.,'wiki')]",
    "//tr[th='Family']//@href[contains(.,'wiki')]",
    "//tr[th='Issue']//@href[contains(.,'wiki')]",
    "//tr[th='Extended family']//@href[contains(.,'wiki')]",
    "//table[@class='wikitable']/tr/td/a/@href[contains(.,'wiki')]",
]


def crawlRelatives(url, xpaths, max=max_urls_to_crawl):
    result = []
    crawled_urls = []
    to_be_crawel = []
    current_url = url
    while len(crawled_urls) < max:
        fetched_urls = []
        res = requests.get(current_url)
        doc = lxml.html.fromstring(res.content)
        crawled_urls.append(current_url)

        for xpath in xpaths:
            fetched_urls += doc.xpath(xpath)

        fetched_urls = set(fetched_urls)
        for url in list(fetched_urls):
            full_url = wiki + url
            result += [[current_url, full_url]]
            if not full_url in to_be_crawel and not full_url in crawled_urls:
                to_be_crawel.append(full_url)

        if len(to_be_crawel) > 0:
            current_url = to_be_crawel.pop(0)
        else:
            result += [[current_url, ""]]
            break

    return result


result = crawlRelatives("https://en.wikipedia.org/wiki/Elizabeth_II", xpath_exp)
with open("Q2.elizabeth.txt", 'w+') as output:
    for entry in result:
        output.write(str(entry[0]) + ', ' + str(entry[1]) + '\n')
