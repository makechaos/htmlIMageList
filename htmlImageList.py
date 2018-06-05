import os
import sys
import glob
import json
from PIL import Image

print('\nUSAGE: python %s <directory> <filter:*.png> <imgsize:WxH>\n'%(sys.argv[0]))

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

userDir = sys.argv[1]
sz = None
filter = '*.png'
for narg in range(2,len(sys.argv)):
  carg = sys.argv[narg].lower()
  if carg.find('imgsize')>=0:
    sz = map(int,carg.split(':')[1].split('x'))
  elif carg.find('filter')>=0:
    filter = carg.split(':')[1]
  
print('getting files from %s, %s ....'%(userDir,filter))
ncrop = 0
flist = []
utags = {}
for pdir,dirs,fils in os.walk(userDir):
  fils = glob.glob( os.path.join(pdir,filter) )
  for fil in fils:
    flist.append(fil)
    fid = len(flist)
    tags = getTags(fil,tagDelim)
    for tag in tags:
      if tag not in utags:
        utags[tag] = 0
      utags[tag] += 1
    if sz is not None:
      im = Image.open(fil)
      if len(sz)==1:
        if sz[0]<im.size[0]:
          im = im.crop((0,0,sz[0],im.size[1]))
          ncrop += 1
          im.save(fil)
      else:
        if sz[0]<im.size[0] or sz[1]<im.size[1]:
          im = im.crop((0,0,sz[0],sz[1]))
          ncrop += 1
          im.save(fil)
print('    ... cropped %d images'%ncrop)
          
print('organize tags ...')
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
stag = tagId.keys()
stag.sort()
for tag in stag:
  ntag += 1
  tagTxt += '<div class="tags" style="width:%dpx;" id="%s" state=0 onclick="tagClick(\'%s\')">%s (%d)</div>'%(max((len(tag)+4)*8,50),tag,tag,tag,utags[tag])

filTxt = ''
filTxt2= ''
nfil = -1
for fil in flist:
  nfil += 1
  filTxt += '<div class="imagehide" id="fid%d" onclick="onSelect(\'fid%d\')" sel="0"><div style="position:absolute;margin:0px;z-index:5;font-size:12;">%s</div><img style="width:100%%;" src="%s"></img></div>\n'%(nfil, nfil, os.path.basename(fil), fil)
  filTxt2+= '<div class="imagehide" id="fid%d" onclick="onSelect(\'fid%d\')" sel="0"><div style="position:absolute;margin:0px;z-index:5;font-size:12;">%s</div><img style="width:100%%;" src="%s"></img></div>\n'%(nfil, nfil, os.path.basename(fil), os.path.basename(fil))
  
def writeOutput(fname, opts):
  tfd = open('imageListTemplate.html','r')
  print('creating output %s'%fname)
  fd = open(fname,'w')
  for tt in tfd.readlines():
    dd = tt
    for opt in opts:
      if dd.find(opt)>=0:
        dd = dd.replace(opt, opts[opt])
    fd.write(dd)
  tfd.close()
  fd.close()
  
writeOutput(os.path.join(userDir,'imagelist.html'), { '{{tagId}}':tagIdTxt,'{{fid2tag}}':fid2tagsTxt, '{{tagTxt}}':tagTxt, '{{filTxt}}':filTxt })
writeOutput(os.path.join(userDir,'imagelist_local.html'), { '{{tagId}}':tagIdTxt,'{{fid2tag}}':fid2tagsTxt, '{{tagTxt}}':tagTxt, '{{filTxt}}':filTxt2 })

print('DONE.')
