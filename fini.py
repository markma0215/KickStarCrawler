# encoding=utf-8
import global_param as gp
from parser import Parser


class Fini(Parser):
    location = {}

    def proLocation(self):
        location = gp.eachProj.select_one('.grey-dark .ksr-icon__location')
        if location is None:
            currency = raw_input("the location is empty, please check the currency\n")
            self.location = {
                'City': ' ',
                'State/Province': ' ',
                'Country': ' ',
                'Currency': currency.encode('utf-8')
            }
            return self.location['City']

        location = location.next_sibling.string.encode('utf-8').strip('\n')
        counCun = gp.getCountryCur(location)
        if counCun[0] == 'US':
            self.location = {
                'City': location.split(', ')[0],
                'State/Province': location.split(', ')[1],
                'Country': counCun[0],
                'Currency': counCun[1]
            }
        else:
            if ',' not in location:
                self.location = {
                    'City': ' ',
                    'State/Province': "",
                    'Country': location.split(', ')[0],
                    'Currency': counCun[1]
                }
            else:
                self.location = {
                    'City': location.split(', ')[0],
                    'State/Province': "",
                    'Country': location.split(', ')[1],
                    'Currency': counCun[1]
                }

        return unicode(self.location['City'], encoding='utf8').encode('utf-8', 'replace')

    def proState(self):
        return self.location['State/Province'].encode('utf-8', 'replace')

    def proCountry(self):
        return self.location['Country'].encode('utf-8', 'replace')

    def proCurrency(self):
        return self.location['Currency'].encode('utf-8', 'replace')

    def proCategory(self):
        category = gp.eachProj.select_one('.grey-dark .ksr-icon__tag').next_sibling.string.encode('utf-8', 'replace').strip('\n')
        return category

    def proGoal(self):
        goal = gp.eachProj.select_one('.navy-500 .money').string
        goal = "".join(c for c in goal if c.isdigit() or c == ',' or c == '.')
        return goal.encode('utf-8', 'replace')

    def proPledged(self):
        pledged = gp.eachProj.select_one('.mb0 .money').string
        pledged = ''.join(c for c in pledged if c.isdigit() or c == ',' or c == '.')
        return pledged.encode('utf-8', 'replace')

    def proBackers(self):
        backers = gp.eachProj.select_one('.border-left .mb0 > h3').string.encode('utf-8', 'replace').strip('\n')
        return backers

    def proCreator(self):
        creator = gp.eachProj.select_one('.creator-name .hero__link').string.encode('utf-8', 'replace').strip('\n')
        return creator

    def getProjectLists(self):
        return {
            "projList": Parser.getProjects(self)
        }

    def getProjectOverview(self):
        return {
            "Projects We Love (0/1)":   Parser.isLoved(self),
            "Campaign Webpage":         Parser.projLink(self),
            "Identifier":               Parser.getID(self)
        }

    def getProjectDetail(self):
        return {
            "Project Name":             Parser.proName(self, '.relative .hero__link'),
            "City":                     self.proLocation(),
            'State/Province':           self.proState(),
            'Country':                  self.proCountry(),
            'Category':                 self.proCategory(),
            '# Updates':                Parser.proUpdates(self, '.js-load-project-updates .count'),
            '# Comments':               Parser.proComments(self),
            'Project Description (No Bold Title, No Pic/Doc/, No table/figure description, No website Links)':
                                        Parser.proDescription(self),
            'Goal':                     self.proGoal(),
            'Pledged':                  self.proPledged(),
            'Currency':                 self.proCurrency(),
            'Minimum Pledge':           Parser.minPledged(self),
            'Maximum Pledge':           Parser.maxPledged(self),
            'Num. Backers':             self.proBackers(),
            'Funding Start (Date Format)': Parser.proStartTime(self),
            'Funding End (Date Format)': Parser.proEndTime(self),
            'Duration':                 Parser.proDuration(self),
            'Project Creator':          self.proCreator()
        }

    def getCreator(self):
        return {
            '# Projects Created':       Parser.creatNum(self),
            '# Projects Backed':        Parser.backNum(self),
            'Identity':                 Parser.proIdentify(self),
            'First Name':               Parser.proFirstName(self),
            'Last Name':                Parser.proLastName(self),
            '# Websites':               Parser.proWebs(self),
            'Facebook (0/1)':           Parser.hasFB(self),
            '# FB Friends':             Parser.friendsFB(self),
            'Project Creator Link': Parser.creatorLink(self)
        }

    def getCreatorDetail(self):
        return {
            '# Creator Comments':       Parser.creatorComments(self),
            'Joined (Date Format)':     Parser.creatorTimeStamp(self),
            'Biography Description (No Bold Title, No Pic/Doc/, No table/figure description, No website Links)':
                                        Parser.creatorBiography(self)
        }