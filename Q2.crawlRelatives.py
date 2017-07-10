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
    crawled_urls = []
    current_url = url
    should_crawl = []
    ret_val = []
    while len(crawled_urls) < max:
        res = requests.get(current_url)
        doc = lxml.html.fromstring(res.content)
        crawled_urls.append(current_url)

        new_urls = []
        for exp in xpaths:
            new_urls += doc.xpath(exp)
        new_urls = set(new_urls)
        # print(current_url)
        if len(new_urls) > 0:
            ret_val += [[current_url, wiki + new_link] for new_link in list(new_urls)]
        else:  # no links
            ret_val += [[current_url, ""]]
        # print(len(crawled_urls), ":", current_url ,":", new_urls)

        for temp_url in new_urls:  # check if should add to queue
            if not should_crawl.__contains__(wiki + temp_url) and not crawled_urls.__contains__(wiki + temp_url):
                should_crawl.append(wiki + temp_url)

        if len(should_crawl) > 0:
            current_url = should_crawl.pop(0)  # pop the first elem in the queue
        else:
            break
    # print("total crawled " , len(crawled_urls), "unique : " , len(set(crawled_urls)))
    return ret_val


result = crawlRelatives("https://en.wikipedia.org/wiki/Elizabeth_II", xpath_exp)
with open("Q2.elizabeth.txt", 'w+') as output:
    for entry in result:
        output.write(str(entry[0]) + ', ' + str(entry[1]) + '\n')


# for i in range(10):
#     print("Highest PR pages: ", list(reversed(sorted(royalPageRank(result).items(), key=operator.itemgetter(1)))))
