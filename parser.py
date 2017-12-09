
import global_param as gp
import bs4
import re

class Parser:

    pledged = []
    timestamp = {}
    proCreateBack = [0, 0]
    identify = ""

    def getProjects(self):
        # print gp.eachProj
        projects = gp.eachProj.select(".js-project-group .js-track-project-card")
        # print len(projects)
        projects = [pro for pro in projects if pro.select_one(".ksr-green-700 .mr2") is None]

        # print len(projects)
        # projects_canclled = [pro for pro in projects
        #                      if pro.select_one(".mt2_3 .mt2").string.encode("utf-8") == 'Funding canceled']
        #
        # projects_unsuccessful = [pro for pro in projects
        #                          if pro.select_one(".mt2_3 .mt2").string.encode("utf-8") == 'Funding unsuccessful']

        fini_projects = [pro for pro in projects
                             if pro.select_one(".mt2_3 .mt2") is None]

        un_projects = [pro for pro in projects
                             if pro.select_one(".mt2_3 .mt2") is not None
                       and (pro.select_one(".mt2_3 .mt2").string.encode("utf-8") == 'Funding canceled'
                    or pro.select_one(".mt2_3 .mt2").string.encode("utf-8") == 'Funding unsuccessful')]

        # print len(projects)
        # print len(un_projects)
        return fini_projects, un_projects

    def isLoved(self):
        # loved = gp.eachProj.select_one(".hover-white")
        loved = gp.eachProj.select_one('.hover-black')
        if loved is None:
            return u'0'.encode("utf-8")
        else:
            return u'1'.encode("utf-8")

    def projLink(self):
        # link = gp.eachProj.select_one('.clamp-3 .navy-700')["href"].encode("utf-8")
        link = gp.eachProj.select_one('.navy-500 .soft-black')['href'].encode('utf-8')
        return link

    def getID(self):
        gp.projID += 1
        return unicode(str(gp.projID), encoding="utf-8")

    def proName(self, cssPath):
        name = gp.eachProj.select_one(cssPath).string.encode("utf-8", 'replace').replace('\n', '').strip()
        return name

    def proLocation(self):
        pass

    def proState(self):
        pass

    def proCountry(self):
        pass

    def proCurrency(self):
        pass

    def proCategory(self):
        pass

    def proUpdates(self, cssPath):
        updates = gp.eachProj.select_one(cssPath).string.encode('utf-8')
        return updates

    def proComments(self):
        comments = gp.eachProj.select_one('.js-load-project-comments .count > data').string.encode('utf-8')
        return comments

    def proDescription(self):
        descp = gp.eachProj.select_one('.full-description')
        allTags = [child for child in descp.descendants if child.name == 'p' or child.name == 'li']

        risk = gp.eachProj.select_one('.js-risks')
        if risk is not None:
            allTags += [child for child in risk.descendants if child.name == 'p' or child.name == 'li']

        allText = []
        for eachTag in allTags:
            for descendant in eachTag.descendants:
                if isinstance(descendant, bs4.element.NavigableString) and descendant.string is not None:
                    allText.append(descendant.string)

        text = "".join(t.strip('\r\n') for t in allText)
        text = text.replace('\r\n', '').replace(u'\xa0', ' ').strip()
        if len(text) > 32200:
            text = text[:32200]
            text = text[:text.rfind(' ')]

        text = ' '.join(t for t in text.split())
        return text.encode('utf-8', 'replace')

    def proGoal(self):
        pass

    def proPledged(self):
        pass

    def minPledged(self):
        pledges = gp.eachProj.select('.pledge__amount .money')
        if pledges == []:
            return " ".encode('utf-8')

        pledges = [''.join(c for c in oneP.string if c.isdigit() or c == ',' or c == '.') for oneP in pledges]
        pledges.sort(key= lambda x : float(x.replace(',', '')))
        self.pledged = pledges

        return self.pledged[0].encode('utf-8')

    def maxPledged(self):
        if self.pledged == []:
            return " ".encode('utf-8')
        return self.pledged[-1].encode('utf-8')

    def proBackers(self):
        pass

    def proStartTime(self):
        timeSlot = gp.eachProj.select('.f5 .js-adjust-time')
        self.timestamp = {
            'start': timeSlot[0].string.encode('utf-8'),
            'end':   timeSlot[1].string.encode('utf-8'),
            'duration': ''.join(c for c in timeSlot[1].next_sibling.string if c.isdigit()).encode('utf-8')
        }

        return self.timestamp['start']

    def proEndTime(self):
        return self.timestamp['end']

    def proDuration(self):
        return self.timestamp['duration']

    def proCreator(self):
        pass

    def creatNum(self):
        number = gp.eachProj.select_one('.created-projects')
        tags = [t for t in number.children if t.string != '\n']
        create = tags[1].string.strip('\n').encode('utf-8').split(' ')[0]
        if create == 'First':
            create = '1'.encode('utf-8')
        self.proCreateBack[0] = create

        back = tags[3].string.strip('\n').encode('utf-8').split(' ')[0]
        if create == 'First':
            back = '1'.encode('utf-8')

        self.proCreateBack[1] = back

        return self.proCreateBack[0]

    def backNum(self):
        return self.proCreateBack[1]

    def proIdentify(self):
        identify = gp.eachProj.select_one('.identity_name').string.encode('utf-8', 'replace').strip('\n')
        if identify.lower() != '(name not available)':
            # print "identify name is  available"
            self.identify = identify.replace('\r\n', '')
            return self.identify
        else:
            self.identify = ""
            return self.identify

    def proFirstName(self):
        if self.identify is "":
            return " ".encode('utf-8')
        else:
            return self.identify.split(" ")[0]

    def proLastName(self):
        if self.identify is "":
            return " ".encode('utf-8')
        else:
            return self.identify.split(" ")[-1]

    def proWebs(self):
        links = gp.eachProj.select_one('.links')
        if links is None:
            return '0'.encode('utf-8')
        else:
            lis = links.find_all('li')
            return str(len(lis)).encode("utf-8")

    def hasFB(self):
        hasFB = gp.eachProj.select_one('.facebook .number > a')
        if hasFB is not None:
            return '1'.encode('utf-8')

        hasFB = gp.eachProj.select_one('.facebook > a')
        if hasFB is not None:
            return '1'.encode('utf-8')
        else:
            return '0'.encode('utf-8')

    def friendsFB(self):
        friends = gp.eachProj.select_one('.facebook .number > a')
        if friends:
            friends = friends.string.encode('utf-8').strip('\n').split(' ')[0]
            return friends
        else:
            return " ".encode('utf-8')

    def creatorLink(self):
        link = gp.eachProj.select_one('.normal .green-dark')['href']
        link = "https://www.kickstarter.com" + link + '/about'
        return link

    def creatorTimeStamp(self):
        try:
            timestamp = gp.eachProj.select_one('.js-adjust-time').string.encode('utf-8').strip('\n')
        except AttributeError:
            notAvailable = gp.eachProj.select_one('.center').string.strip().encode('utf-8')
            if notAvailable == 'Sorry! This person is no longer active on Kickstarter.':
                return ' '.encode('utf-8')
        else:
            return timestamp

    def creatorComments(self):
        comments = gp.eachProj.select_one('.js-comments-link .count')
        if comments is None:
            return ' '.encode('utf-8')
        else:
            comments = comments.string.encode('utf-8').strip('\n')
        return comments

    def creatorBiography(self):
        bioTags = gp.eachProj.select('.col-sm-15-20 > p')
        bio = []
        for eachPTag in bioTags:
            # print eachPTag
            for eachText in eachPTag.descendants:
                # print eachPTag
                if eachText.string is not None and isinstance(eachText, bs4.element.NavigableString):
                    # print 'add string ' + eachText.string
                    bio.append(eachText.string)

        # print bio
        text = ' '.join(bioStr.replace('\r\n', '').strip() for bioStr in bio if bioStr is not None)
        text = ' '.join(t for t in text.split())

        if text == '':
            print "no biography in this creator"
        # import sys
        # sys.exit(1)
        return text.encode('utf-8', 'replace')

    def getProjectLists(self):
        pass

    def getProjectOverview(self):
        pass

    def getProjectDetail(self):
        pass

    def getCreator(self):
        pass

    def getCreatorDetail(self):
        pass




