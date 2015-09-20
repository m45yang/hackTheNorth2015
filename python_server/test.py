count = 100
search = api.GetSearch(term='china', lang='en', result_type='recent', count , max_id='')
for t in search:
 #print t.user.screen_name + ' (' + t.created_at + ')'
 #Add the .encode to force encoding
 print t.text.encode('utf-8')
 print ''


 #finding popular tweets
 countpop = 3
search = api.GetSearch(term='china', lang='en', result_type='popular', countpop , max_id='')
for t in search:
 print t.user.screen_name + ' (' + t.created_at + ')'
 #Add the .encode to force encoding
 print t.text.encode('utf-8')
 print ''