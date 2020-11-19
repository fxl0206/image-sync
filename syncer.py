#!/bin/python
import getopt
import commands
import sys
import json
import re

helpInfo = 'syncer.py -s registry1.xxx.xx -t registry2.xxx.xx:6060'
def parseUrl(uri):
    matchObj = re.match( r'(http[s]://)(.*)', uri, re.M|re.I)
    if matchObj:
      print matchObj.group(1),'----',matchObj.group(2)
      sys.exit()
    else:
      print uri
      sys.exit()
def main(argv):
  source = ''
  target = ''
  try:
    opts, args = getopt.getopt(argv,"hs:t:",["source=","target="])
  except getopt.GetoptError:
    print(helpInfo)
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
       print(helpInfo)
       sys.exit()
    elif opt in ("-s", "--source"):
       parseUrl(arg)
       source = arg
    elif opt in ("-t", "--target"):
       target = arg
  print source,target
  val = commands.getoutput('curl -k -s '+source+'/v2/_catalog')
  print val
  load_json=json.loads(val)
  for i in load_json["repositories"]:
      (status,val)=commands.getstatusoutput('curl -s '+source+'/v2/'+i+'/tags/list')
      if status==0 :
        meta=json.loads(val)
        if meta.has_key('name') : 
          for j in meta["tags"]:
            tokens = j.split('/')
            imageUri=i+':'+j
            sourceUri=source+'/'+imageUri
            if len(tokens) == 1:
              imageUri='library/'+imageUri
            targetUri=target+'/'+imageUri
            cmd_str='docker pull '+sourceUri+' && docker tag '+sourceUri+' '+targetUri
            cmd_str=cmd_str+' && docker push '+targetUri+' && docker rmi '+sourceUri+' && docker rmi '+targetUri
            print(cmd_str)

if __name__ == "__main__":
   main(sys.argv[1:])
