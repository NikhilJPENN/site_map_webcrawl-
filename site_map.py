#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 16:31:20 2019

@author: jnikhil

To run the file open the command window and cd to folder 
command: python site_map.py https://www.mozilla.org/en-US/ 2

"""

from urllib.request import urlopen  
from urllib import parse
from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
import re
import json
import sys
 
class PageParser():           
        
        #This creates object for to be parsed for every url page
                    
    def getLinks(self, url):                # parsing each url page and getting links on the page
        
    
        self.links = []
        self.indomain = []
        self.baseUrl = url
        
        response = requests.get(url)  
        
        parts = urlsplit(url)
        base = "{0.netloc}".format(parts)
        strip_base = base.replace("www.", "")
     
        path = url[:url.rfind('/')+1] if '/' in parts.path else url
            
        soup = BeautifulSoup(response.text, "html.parser") 
        
        for link in soup.find_all('a'):    
        
            anchor = link.attrs["href"] if "href" in link.attrs else ''
                  
            if anchor.startswith('/'):
                newUrl = parse.urljoin(self.baseUrl, anchor)
                local = newUrl
                
            elif strip_base in anchor:
                newUrl = anchor
                local = newUrl
            
            elif not anchor.startswith('http'):
                newUrl = path + anchor
                local = newUrl
            else:
                newUrl = anchor           
        
            self.links = self.links + [newUrl]           # all links in domain and out domain 
            self.indomain = self.indomain + [local]      # only local links that need to be crawl based on depth 
            
        return (list(set(self.links)), list(set(self.indomain)))   #return both links on the page and links with same domain
    
    def getImage(self,url):                              #Parsing a url page for images
        
        self.images = []
    
        html = urlopen(url)
        bs = BeautifulSoup(html, 'html.parser')
       
        imgs = bs.find_all('img', {'src':re.compile('.')})
        
        for image in imgs: 
            self.images += [(image['src'])]    
        
        return self.images          #return images on the page'''


def  build_site_map(url, max_depth):  
    
    visited = []
    pages_to_visit = [url]
    visited_links = 0
    j_list = []
    '''
    This function takes two arguments url (from where start site map) and maximum number of pages to be visited 
    '''
    while visited_links < max_depth and pages_to_visit != []:
        visited_links = visited_links +1
        dict_={}    
        url = pages_to_visit[0]
        pages_to_visit = pages_to_visit[1:]
        images_on_page = []
        
        try:
        
            parser = PageParser()
            
            links,domain_links = parser.getLinks(url)            
            images = parser.getImage(url) 
            
            visited = visited + [url]
            pages_to_visit = pages_to_visit + domain_links            
            pages = set(pages_to_visit)-set(visited)  # remove visited urls          
            pages_to_visit = [ele for ele in pages_to_visit if ele in pages]
            
            images_on_page = images 
            
            dict_['page_url'] = url
            dict_['links'] = links
            dict_['images'] = images_on_page
            j_list.append(dict_)
            
        except:
            print("Error")
            
                
    return (json.dumps(j_list))      #returns json file 

def main():

    json_data = build_site_map(url,max_depth)       
    parsed = json.loads(json_data)
    print(json.dumps(parsed, indent=4, sort_keys=False))  # prints output json file 
     
    
if __name__ == "__main__":
    url = (sys.argv[1])  
    max_depth = int(sys.argv[2])        # give command line arguments url and max depth 
    main()                              # in command window python site_map.py https://www.mozilla.org/en-US/ 2
