import random


def royalPageRank(listOfPairs, rounds=1000):
    links = {}
    rank = {}
    for [url, link] in listOfPairs:
        if link == '':
            continue
        if links.__contains__(url):
            links[url] += [link]
        else:
            links[url] = [link]
    # for i in links:
    #     print(i, links[i])
    current_url = listOfPairs[0][0]  # start page
    for i in range(rounds):
        # print("round : ", i)
        if rank.__contains__(current_url):
            rank[current_url] += 1
        else:
            rank[current_url] = 1
        if random.random() < 0.8 and links.__contains__(current_url):  # go to a linked url
            next_url = links[current_url][random.randint(0, len(links[current_url]) - 1)]
        else:  # random>0.8 or no links from current url
            next_url = links.keys()[random.randint(0, len(links.keys()) - 1)]

        current_url = next_url
    for key in rank.keys():
        rank[key] = rank[key] * 1.0 / rounds
    # print("probs : ", sorted(rank.values(),reverse=True))
    # print("visited ",len(rank) ," diff urls")
    return rank

# print royalPageRank(Q2.crawlRelatives(Q2.queen_url, Q2.xpath_exp, max=50))
