import urlparse
import urllib
import os
import re
from BeautifulSoup import BeautifulSoup

directory_to_store = "C:\\drdobbs\\";

url = 'http://www.drdobbs.com/cpp/padding-and-rearranging-structure-member/240007649?pgno=2'#
urls = [url]        # list of nodes to visit

visited = {}       # keep track of visited nodes
 

os.chdir(directory_to_store)


#define the function, returning a boolean, which will determine the requirements for adding a url to the list of things to process
def should_add(cur_url):
    #cur_url is a string with the current URL of a possible page to crawl. 

    # for the drdobbs example, I only want the /cpp/ section and I don't care about the discussions page (disqus_thread)
    return (cur_url.startswith("http://www.drdobbs.com/cpp/") )and "disqus_thread" not in cur_url


while len(urls) > 0:
    
    cur_url = urls[-1];
    try:
        htmltext = urllib.urlopen(cur_url).read()
    except:
        print 'Could not open: {}'.format(cur_url)

    soup = BeautifulSoup(htmltext)


    for tag in soup.findAll('a',href=True):
      cur_tag = tag['href'];
      if should_add(urlparse.urljoin(cur_url,cur_tag)):

                
           #clean the file and make appropriate adjustments to the HTML
          to_add = urlparse.urljoin(cur_url,tag['href']);
          o = urlparse.urlparse(to_add);

          path = o.geturl()[o.geturl().find(o[2]) : ] # get the identifier
          cleaned_filename = re.sub("[/\\:?*<>|\"]","__",''.join(path)) # clean the filename so that it can be stored without issue 
          htmltext = htmltext.replace(''.join(path),cleaned_filename) #edit the HTML to refernece the clean version 
          if cur_tag not in visited:
                  urls.append(to_add);
                  visited[cur_tag] = True;


    cur_tag = urls.pop(); #urls is acting as a stack.. although a queuing mechanism would work here as well
    o = urlparse.urlparse(cur_tag);
    path = o.geturl()[o.geturl().find(o[2]) : ]
    cleaned_filename =  re.sub("[/\\:?*<>|\"]","__",''.join(path))
    write_out = file(cleaned_filename,"w");
    write_out.write(htmltext);
    write_out.close();
    print "Writing out file " + cleaned_filename;




   
   
print visited