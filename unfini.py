
import global_param as gp
from parser import Parser
from paramError import ParamError


class Unfini(Parser):
    location = {}

    def proLocation(self):
        location = gp.eachProj.select('.col-sm-22-24 .py3-lg .items-center > a')
        for each in location:
            if 'ref=city' in each['href']:
                location = each.contents[1].string.replace('\n', '').strip().encode('utf-8', 'replace')
                break

        if isinstance(location, list):
            if 'US' in gp.eachProj.select_one('.js-pledged').string:
                currency = 'USD'
            else:
                currency = raw_input("location is not available, put check currency\n")

            self.location = {
                'City': ' ',
                'State/Province': ' ',
                'Country': ' ',
                'Currency': currency.encode('utf-8')
            }
            return self.location['City'].encode('utf-8')

        counCun = gp.getCountryCur(location)
        if counCun[0] == 'US':
            self.location = {
                'City': location.split(', ')[0],
                'State/Province': location.split(', ')[1],
                'Country': counCun[0],
                'Currency': counCun[1]
            }

        else:
            if len(location.split(', ')) == 1:
                self.location = {
                    'City': ' ',
                    'State/Province': ' ',
                    'Country': location,
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
        category = gp.eachProj.select('.col-sm-22-24 .py3-lg .items-center > a')
        for each in category:
            if 'ref=category' in each['href']:
                category = each.contents[1].string.replace('\n', '').strip().encode('utf-8', 'repalce')
                break

        if isinstance(category, list):
            choice = raw_input('category is not available, put category as empty and continue? yes, no\n')
            if choice == 'yes':
                return ' '.encode('utf-8')
            else:
                raise ParamError('Category is not available')

        return category

    def proGoal(self):
        goal = gp.eachProj.select_one('.lh3-lg .money').string
        goal = ''.join(c for c in goal if c.isdigit() or c == ',' or c == '.')
        return goal.encode('utf-8')

    def proPledged(self):
        pledged = gp.eachProj.select_one('.js-pledged').string
        pledged = ''.join(c for c in pledged if c.isdigit() or c == ',' or c == '.')
        return pledged.encode('utf-8')

    def proBackers(self):
        backers = gp.eachProj.select_one('.js-backers_count').string.encode('utf-8').strip('\n')
        return backers

    def proCreator(self):
        creator = gp.eachProj.select_one('.navy-700 .remote_modal_dialog').string.encode('utf-8').strip('\n')
        return creator

    def getProjectLists(self):
        return {
            "projList": Parser.getProjects(self)
        }

    def getProjectOverview(self):
        return {
            "Projects We Love (0/1)": Parser.isLoved(self),
            "Campaign Webpage": Parser.projLink(self),
            "Identifier": Parser.getID(self)
        }

    def getProjectDetail(self):
        return {
            "Project Name": Parser.proName(self, '.hide .type-28-sm'),
            "City": self.proLocation(),
            'State/Province': self.proState(),
            'Country': self.proCountry(),
            'Category': self.proCategory(),
            '# Updates': Parser.proUpdates(self, '.js-load-project-updates .count'),
            '# Comments': Parser.proComments(self),
            'Project Description (No Bold Title, No Pic/Doc/, No table/figure description, No website Links)':
                Parser.proDescription(self),
            'Goal': self.proGoal(),
            'Pledged': self.proPledged(),
            'Currency': self.proCurrency(),
            'Minimum Pledge': Parser.minPledged(self),
            'Maximum Pledge': Parser.maxPledged(self),
            'Num. Backers': self.proBackers(),
            'Funding Start (Date Format)': Parser.proStartTime(self),
            'Funding End (Date Format)': Parser.proEndTime(self),
            'Duration': Parser.proDuration(self),
            'Project Creator': self.proCreator()
        }

    def getCreator(self):
        return {
            '# Projects Created': Parser.creatNum(self),
            '# Projects Backed': Parser.backNum(self),
            'Identity': Parser.proIdentify(self),
            'First Name': Parser.proFirstName(self),
            'Last Name': Parser.proLastName(self),
            '# Websites': Parser.proWebs(self),
            'Facebook (0/1)': Parser.hasFB(self),
            '# FB Friends': Parser.friendsFB(self),
            'Project Creator Link': Parser.creatorLink(self)
        }

    def getCreatorDetail(self):
        return {
            'Joined (Date Format)': Parser.creatorTimeStamp(self),
            '# Creator Comments': Parser.creatorComments(self),
            'Biography Description (No Bold Title, No Pic/Doc/, No table/figure description, No website Links)':
                Parser.creatorBiography(self)
        }