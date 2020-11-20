#!/bin/python
import getopt
import commands
import sys
import json
import re
import os

helpInfo = 'syncer.py -s https://registry1.xxx.xx -t registry2.xxx.xx:6060'
def parseUrl(uri):
    matchObj = re.match( r'(https?://)(.*)', uri, re.M|re.I)
    if matchObj:
      return matchObj.group(1),matchObj.group(2)
    else:
      print(uri+' must start with http or https')
      sys.exit()

def parseOpts(argv):
  sProtocol=''
  source = ''
  target = ''
  model = ''
  try:
    opts, _ = getopt.getopt(argv,"hs:t:m:",["source=","target=","model="])
  except getopt.GetoptError:
    print(helpInfo)
    sys.exit(2)
  print(opts)
  for opt, arg in opts:
    if opt == '-h':
       print(helpInfo)
       sys.exit()
    elif opt in ("-s", "--source"):
       (sProtocol,source) = parseUrl(arg)
    elif opt in ("-t", "--target"):
       target = arg
    elif opt in ("-m", "--model"):
       model= arg
  print (source,target,model)
  return sProtocol,source,target,model

def main(argv):
  (sProtocol,source,target,model) = parseOpts(argv)
  val = commands.getoutput('curl -k -s '+sProtocol+source+'/v2/_catalog')
  print(val)
  load_json=json.loads(val)
  for i in load_json["repositories"]:
      (status,val)=commands.getstatusoutput('curl -s -k '+sProtocol+source+'/v2/'+i+'/tags/list')
      if status==0 :
        meta=json.loads(val)
        if meta.has_key('name') : 
          for j in meta["tags"]:
            tokens = i.split('/')
            imageUri=i+':'+j
            sourceUri=source+'/'+imageUri
            if len(tokens) == 1:
              imageUri='library/'+imageUri
            targetUri=target+'/'+imageUri
            cmd_str = ''
            if model == 'sk':
              cmd_str='skopeo copy docker://'+sourceUri+' docker://'+targetUri
            else:
              cmd_str='docker pull '+sourceUri+' && docker tag '+sourceUri+' '+targetUri
              cmd_str=cmd_str+' && docker push '+targetUri+' && docker rmi '+sourceUri+' && docker rmi '+targetUri
            print(cmd_str)
            os.system(cmd_str)

if __name__ == "__main__":
   main(sys.argv[1:])
