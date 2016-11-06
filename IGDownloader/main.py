import urllib
import json
import re
import os
import sys
from bs4 import BeautifulSoup

dir = os.getcwd()

def get_account_info(username):
    url = "http://instagram.com/"
    html = urllib.urlopen(url+username)
    soup = BeautifulSoup(html, "lxml")

    print "      [+] Checking Username ..."
    title = soup.title.string.replace("\n","").replace(" ","")
    if(title == "Instagram"):
        print "          [!] Username Not Found"
        sys.exit()
    else:
        if not os.path.exists(username):
            os.makedirs(username)

    folder = os.path.join(dir, "%s" % username)
    script = soup.find('script', text=re.compile('window\._sharedData'))
    json_text = re.search(r'^\s*window\._sharedData\s*=\s*({.*?})\s*;\s*$',
                      script.string, flags=re.DOTALL | re.MULTILINE).group(1)
    data = json.loads(json_text)

    print "      [+] Getting Info User ..."
    dt = data['entry_data']['ProfilePage']
    info_fullname = dt[0]['user']['full_name']
    info_follow = dt[0]['user']['follows']['count']
    info_followed = dt[0]['user']['followed_by']['count']
    info_private = dt[0]['user']['is_private']
    info_profil_pic = dt[0]['user']['profile_pic_url']
    info_count = dt[0]['user']['media']['count']
    urllib.urlretrieve(info_profil_pic,os.path.join(folder, os.path.basename("profil")))
    print "          [-] User Info"
    print "              Name       : %s"%(info_fullname)
    print "              Post       : %s"%(info_count)
    print "              Followers  : %s"%(info_followed)
    print "              Following  : %s"%(info_follow)
    if(info_private == "False"):
        print "              [!] Account Is Private"
        sys.exit()
    elif(info_count == 0):
        print "              [!] No Post"
        sys.exit()
    else:
        data_post = dt[0]['user']['media']
        for i in data_post['nodes']:
            post_id = i['code']
            is_video = i['is_video']
            comment = i['comments']['count']
            like = i['likes']['count']
            post_url = i['display_src']
            check_vid= str(is_video)
            if(check_vid == "False"):
                type = "Image"
            else:
                type = "Video"
            print "\n"
            print "          [-] Post Info"
            print "              Id         : %s" % (post_id)
            print "              Type       : %s" % (type)
            print "              Like       : %s" % (like)
            print "              Comment    : %s" % (comment)
            if(type == "Image"):
                sep = '?'
                uri_fix = post_url.split(sep, 1)[0]
                urllib.urlretrieve(uri_fix, os.path.join(folder, os.path.basename(post_id)))
            else:
                p="p/"
                uri = url+p+post_id
                get_vid = urllib.urlopen(uri)
                soup_vid = BeautifulSoup(get_vid, "lxml")
                script = soup_vid.find('script', text=re.compile('window\._sharedData'))
                json_text = re.search(r'^\s*window\._sharedData\s*=\s*({.*?})\s*;\s*$',
                                      script.string, flags=re.DOTALL | re.MULTILINE).group(1)
                data_vid = json.loads(json_text)
                dt_vid = data_vid['entry_data']['PostPage']
                url_vid = dt_vid[0]['media']['video_url']
                urllib.urlretrieve(url_vid, os.path.join(folder, os.path.basename(post_id)))
            print "              [!] Post Downloaded"

def main():
    print '''
      -------------------------
    | Instagram Post Downloader
    | -------------------------
    |           qianna@null.net
    | -------------------------
    | Required : -Python 2.7
    |            -BeautifulSoup
      -------------------------
    '''
    username = raw_input("    > Enter Username (without @) : ")
    get_account_info(username)

main()