import random


def royalPageRank(listOfPairs, rounds=1000, follow_probability=0.8):
    links = {}
    ranks = {}
    for [url, link] in listOfPairs:
        if link == '':
            continue

        init_links(link, links, url)

    current_url = listOfPairs[0][0]
    for i in range(rounds):
        init_rank(current_url, ranks)
        next_url = fetch_next_url(current_url, follow_probability, links)
        current_url = next_url

    for key in ranks.keys():
        ranks[key] = ranks[key] * 1.0 / rounds

    return ranks


def init_links(link, links, url):
    if url in links:
        links[url] += [link]
    else:
        links[url] = [link]


def init_rank(current_url, ranks):
    if current_url in ranks:
        ranks[current_url] += 1
    else:
        ranks[current_url] = 1


def fetch_next_url(current_url, follow_probability, links):
    if random.random() < follow_probability and current_url in links:
        next_url = links[current_url][random.randint(0, len(links[current_url]) - 1)]
    else:
        next_url = links.keys()[random.randint(0, len(links.keys()) - 1)]
    return next_url
