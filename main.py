# -*- coding: utf-8 -*-
import global_param as gp
from unfini import Unfini
from fini import Fini
from parser import Parser
import sys
import traceback

def main():

    for pageNum in range(gp.page, 201):
        print "Get into page %s" % str(pageNum)
        url = gp.k10_k100_StartLink[:-1] + str(pageNum)
        gp.listPage(url)
        parser = Parser()
        unfini = Unfini()
        fini = Fini()

        finiPorj, unfiniProj = parser.getProjects()
        # print len(finiPorj)
        # print len(unfiniProj)

        if not finiPorj and not unfiniProj:
            print "page " + str(pageNum) + " does not contain projects that we want"
            continue
        else:
            try:
                for i in range(0, len(finiPorj)):
                    if i < gp.threshold: continue
                    print "in finished projects, number %s is being crawled" % str(i)
                    data = {}
                    # print finiPorj[i]
                    gp.eachProj = finiPorj[i]
                    overview = fini.getProjectOverview()
                    print overview
                    data.update(overview)

                    # print "refresh begin"
                    gp.refreshWebPage(overview['Campaign Webpage'])
                    # print "refresh end"
                    proDetail = fini.getProjectDetail()
                    data.update(proDetail)

                    # print "refresh begin"
                    projectLink = overview['Campaign Webpage']
                    if '?' in projectLink:
                        projectLink = projectLink[:projectLink.rfind('?')]
                    gp.refreshWebPage(projectLink + '/creator_bio')
                    # print "refresh end"
                    creator = fini.getCreator()
                    data.update(creator)

                    gp.refreshWebPage(creator['Project Creator Link'])
                    creatorDetail = fini.getCreatorDetail()
                    data.update(creatorDetail)
                    gp.writeCrawlData(data)

                for i in range(0, len(unfiniProj)):
                    if i < gp.threshold: continue
                    print "in UNfinished projects, number %s is being crawled" % str(i)
                    data = {}
                    gp.eachProj = unfiniProj[i]
                    overview = unfini.getProjectOverview()
                    print overview
                    data.update(overview)

                    gp.refreshWebPage(overview['Campaign Webpage'])
                    proDetail = unfini.getProjectDetail()
                    data.update(proDetail)

                    projectLink = overview['Campaign Webpage']
                    if '?' in projectLink:
                        projectLink = projectLink[:projectLink.rfind('?')]
                    gp.refreshWebPage(projectLink + '/creator_bio')
                    # gp.refreshWebPage(overview['Campaign Webpage'] + '/creator_bio')
                    creator = unfini.getCreator()
                    data.update(creator)

                    gp.refreshWebPage(creator['Project Creator Link'])
                    creatorDetail = unfini.getCreatorDetail()
                    data.update(creatorDetail)
                    gp.writeCrawlData(data)

            except:
                print traceback.print_exc(file=sys.stdout)
                # print gp.countryMap
                print 'page is %s' % pageNum
                print 'threshold is %s' % i
                print 'project id is %s' % (gp.projID - 1)
                sys.exit(1)

        gp.threshold = 0


if __name__ == "__main__":

    main()

    # test program
    # session = dryscrape.Session()
    # session.visit('https://www.kickstarter.com/projects/alexklein/creative-computing-for-all')
    # doc = session.body()
    # gp.soup = BeautifulSoup(doc, "lxml")
    # descp = gp.soup.select_one('.full-description')
    # allTags = [child for child in descp.descendants if child.name == 'p' or child.name == 'li']
    #
    # risk = gp.soup.select_one('.js-risks')
    # allTags += [child for child in risk.descendants if child.name == 'p' or child.name == 'li']
    #
    # allText = []
    # for eachTag in allTags:
    #     for descendant in eachTag.descendants:
    #         if isinstance(descendant, bs4.element.NavigableString) and descendant.string is not None:
    #             allText.append(descendant.string)
    #
    # text = "".join(t.strip('\n') for t in allText)
    # print text.encode('utf-8')
    # l1 = []
    # print not l1
    # import pycountry
    # print pycountry.countries.lookup('DE')
    # print list(pycountry.currencies)

    # import requests
    # from bs4 import BeautifulSoup
    # res = requests.get('https://www.kickstarter.com/projects/1765443095/world-friends-changing-the-way-children-learn-and')
    # soup = BeautifulSoup(res.content, 'html.parser')
    # p = soup.select_one('.full-description > p strong').next_sibling
    # sp = p.string
    # sps = ' '.join(s.replace(u'\xa0', ' ') for s in sp.split('\r\n'))
    # # print len(sps)
    # # print sp.replace('\r\n', '')
    # # print sps
    # # sps = sp.split('\r\n')
    # # print sps
    # print sps