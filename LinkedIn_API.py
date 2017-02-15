from linkedin import linkedin

API_KEY = 'wFNJekVpDCJtRPFX812pQsJee-gt0zO4X5XmG6wcfSOSlLocxodAXNMbl0_hw3Vl'
API_SECRET = 'daJDa6_8UcnGMw1yuq9TjoO_PMKukXMo8vEMo7Qv5J-G3SPgrAV0FqFCd0TNjQyG'
RETURN_URL = 'http://localhost:8000'

authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
print authentication.authorization_url  # open this url on your browser
application = linkedin.LinkedInApplication(authentication)

application.get_profile(selectors=['id', 'first-name', 'last-name', 'location', 'distance', 'num-connections', 'skills', 'educations'])
                                  {u'distance': 0,
                                   u'educations': {u'_total': 1,
                                    u'values': [{u'activities': u'This is my activity and society field',
                                      u'degree': u'graduate',
                                      u'endDate': {u'year': 2009},
                                      u'fieldOfStudy': u'computer science',
                                      u'id': 42611838,
                                      u'notes': u'This is my additional notes field',
                                      u'schoolName': u'\u0130stanbul Bilgi \xdcniversitesi',
                                      u'startDate': {u'year': 2004}}]},
                                   u'firstName': u'ozgur',
                                   u'id': u'COjFALsKDP',
                                   u'lastName': u'vatansever',
                                   u'location': {u'country': {u'code': u'tr'}, u'name': u'Istanbul, Turkey'},
                                   u'numConnections': 13}
                         
application.get_companies(company_ids=[1035], universal_names=['apple'], selectors=['name'], params={'is-company-admin': 'true'})
# 1035 is Microsoft
# The URL is as follows: https://api.linkedin.com/v1/companies::(1035,universal-name=apple)?is-company-admin=true

                                  {u'_total': 2,
                                   u'values': [{u'_key': u'1035', u'name': u'Microsoft'},
                                    {u'_key': u'universal-name=apple', u'name': u'Apple'}]}

                                  # Get the latest updates about Microsoft
                                  application.get_company_updates(1035, params={'count': 2})
                                  {u'_count': 2,
                                   u'_start': 0,
                                   u'_total': 58,
                                   u'values': [{u'isCommentable': True,
                                     u'isLikable': True,
                                     u'isLiked': False,
                                     u'numLikes': 0,
                                     u'timestamp': 1363855486620,
                                     u'updateComments': {u'_total': 0},
                                     u'updateContent': {u'company': {u'id': 1035, u'name': u'Microsoft'},
                                      u'companyJobUpdate': {u'action': {u'code': u'created'},
                                       u'job': {u'company': {u'id': 1035, u'name': u'Microsoft'},
                                        u'description': u'Job Category: SalesLocation: Sacramento, CA, USJob ID: 812346-106756Division: Retail StoresStore...',
                                        u'id': 5173319,
                                        u'locationDescription': u'Sacramento, CA, US',
                                        u'position': {u'title': u'Store Manager, Specialty Store'},
                                        u'siteJobRequest': {u'url': u'http://www.linkedin.com/jobs?viewJob=&jobId=5173319'}}}},
                                     u'updateKey': u'UNIU-c1035-5720424522989961216-FOLLOW_CMPY',
                                     u'updateType': u'CMPY'},
                                    {u'isCommentable': True,
                                     u'isLikable': True,
                                     u'isLiked': False,
                                     u'numLikes': 0,
                                     u'timestamp': 1363855486617,
                                     u'updateComments': {u'_total': 0},
                                     u'updateContent': {u'company': {u'id': 1035, u'name': u'Microsoft'},
                                      u'companyJobUpdate': {u'action': {u'code': u'created'},
                                       u'job': {u'company': {u'id': 1035, u'name': u'Microsoft'},
                                        u'description': u'Job Category: Software Engineering: TestLocation: Redmond, WA, USJob ID: 794953-81760Division:...',
                                        u'id': 5173313,
                                        u'locationDescription': u'Redmond, WA, US',
                                        u'position': {u'title': u'Software Development Engineer in Test, Senior-IEB-MSCIS (794953)'},
                                        u'siteJobRequest': {u'url': u'http://www.linkedin.com/jobs?viewJob=&jobId=5173313'}}}},
                                     u'updateKey': u'UNIU-c1035-5720424522977378304-FOLLOW_CMPY',
                                     u'updateType': u'CMPY'}]}
