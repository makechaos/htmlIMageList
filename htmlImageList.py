import os
import sys
import glob
import json

def getTags(fname, delims):
  tags = [fname]
  for delim in delims:
    ntags = set()
    for tag in tags:
      for ent in tag.split(delim):
        ntags.add(ent.lower())
    tags = list(ntags)
  return tags
tagDelim = [',','-','_','\\','.']

flist = []
utags = {}
userDir = sys.argv[1]
for pdir,dirs,fils in os.walk(userDir):
  fils = glob.glob(pdir+'\\*.png')
  for fil in fils:
    flist.append(fil)
    fid = len(flist)
    tags = getTags(fil,tagDelim)
    for tag in tags:
      if tag not in utags:
        utags[tag] = 0
      utags[tag] += 1

tagId = dict()
for tag in utags:
  tagId[tag] = len(tagId.keys())
  
fid2tags = []
for fil in fils:
  tags = getTags(fil,tagDelim)
  tid = set()
  for tag in tags:
    tid.add(tagId[tag])
  fid2tags += [ list(tid) ]
fid2tagsTxt = 'var fid2tag='+json.dumps(fid2tags)+';'

print('# of files : %d'%len(fid2tags))
print('# of tags  : %d'%len(tagId.keys()))

tagIdTxt = 'var tagId = ' + json.dumps(tagId) + ';'

tagTxt = ''
ntag = -1
for tag in tagId.keys():
  ntag += 1
  tagTxt += '<div class="tags" style="width:%dpx;" id="%s" state=0 onclick="tagClick(\'%s\')">%s (%d)</div>'%(max((len(tag)+4)*8,50),tag,tag,tag,utags[tag])

filTxt = ''
nfil = -1
for fil in flist:
  nfil += 1
  filTxt += '<div class="imagehide" id="fid%d"><div style="position:absolute;margin:0px;z-index:5;font-size:12;">%s</div><img style="width:100%%;" src="%s"></img></div>\n'%(nfil, os.path.basename(fil), fil)

tfd = open('htmlImageTemplate.html','r')  
fd = open(userDir + '\\imagelist.html','w')
for tt in tfd.readlines():
  dd = tt
  if dd.find('{{fid2tag}}')>=0:
    dd = dd.replace('{{fid2tag}}',fid2tagsTxt)
    dd = dd + '\n' + tagIdTxt + '\n'
  elif dd.find('{{tagTxt}}')>=0:
    dd = dd.replace('{{tagTxt}}',tagTxt)
  elif dd.find('{{filTxt}}')>=0:
    dd = dd.replace('{{filTxt}}',filTxt)
  fd.write(dd)
tfd.close()
fd.close()
 
