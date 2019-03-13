from bs4 import BeautifulSoup
import requests
import json
"""
TAG HUNTER
@params str url
@params str sitename
@param list tagContent[str(tag), dict(features)]
@params list findparams [[str(tag), dict(features), (optional)str(parameter to get the content)], [str(tag), dict(features), (optional)str(parameter to get the content)], [str(tag), dict(features), (optional)str(parameter to get the content)]]
"""

class TagHunter:
  def __init__(self, url, sitename, tagContent):
    self.sitename = sitename
    self.url = []
    self.confirmPage = True
    self.confirmAnalyze = True
    self.confirmUrls = True
    self.urlInicial = url
    self.forUrls = []
    self.tagContent = tagContent
    self.url.append(url)
    self.pages = []
    self.content = []
    self.dirtyContent = []
    self.urls_ja_escaneadas = []


  def main(self):
    count = 0
    while self.confirmPage == True or self.confirmAnalyze == True:
      self.confirmPage = self.GetPages()
      self.confirmAnalyze = self.Analyze()
    self.confirmClean = self.CleanContent()
  def Analyze(self):
    try:
      if len(self.pages) != 0:
        pageForAnalyze = self.pages.pop()
      else:
        return False 
      page = pageForAnalyze[1]
      tempContent = []
      i=0
   
      for z in self.tagContent:  
        result = page.find_all(z[0])
        print(result)
        for y in result:
          tempContent.append(y)
      self.dirtyContent.append(tempContent)
    except KeyError:
      print(KeyError)
      return False
    else:
      return True

  def CleanContent(self):
    while True:
      try:
        if len(self.dirtyContent) != 0:
          forAnalyze = self.dirtyContent.pop()
        else:
          return True
        for x in self.tagContent:
          for key,val in x[1].items():
            tempContent = []
            for z in forAnalyze:
              
              if z.get(key)== val:
                tempContent.append(z) 
          if len(x) == 3:  
            for z in range(0, len(tempContent)):
              tempContent[z] = tempContent[z].get(x[2])
        
        for z in range(0, len(tempContent)):
          self.content.append(tempContent[z])
      except KeyError:
        return False
      else:
        
        pass
    return True
  def GetPages(self):
    try:
      tempUrl = []
      tempPages = []
      self.nUrl = len(self.url)
      for x in range(0, self.nUrl):
        try:
          self.nUrl = len(self.url)
          for x in range(0, self.nUrl):
            try:
              tempUrl = self.url.pop()
            except KeyError:
              break
            else:
              if tempUrl not in self.urls_ja_escaneadas:
                  print(tempUrl)
                  self.urls_ja_escaneadas.append(tempUrl)
                  resposta = requests.get(tempUrl)
                  if resposta.status_code == 200:
                    try:

                      tempPages.append(tempUrl)
                      try:
                        tempPages.append(BeautifulSoup(resposta.content, "html.parser"))
                      except TypeError:
                        pass
                      else:
                        self.pages.append(tempPages)   
                        bs = BeautifulSoup(resposta.content, "html.parser")
                        for link in bs.find_all('a'):
                          if link["href"].startswith(self.urlInicial):
                            self.url.append(link["href"])
                          elif link["href"].startswith("/") and tempUrl+link["href"] != tempUrl+"/":
                            self.url.append(tempUrl + link["href"])
                          elif link["href"].startswith(tempUrl) and tempUrl+link["href"] != tempUrl+"/":
                            self.url.append(link["href"])
                    except KeyError:
                      pass
          
        except KeyError:
          pass
    except KeyError: ##1
      return False    
  def export(self, data):
    with open(data, 'a') as outfile:
      json.dump(json.dumps(self.content), outfile)

site = TagHunter("https://jivoi.github.io", "jivoi.github", [["code",{"class":"language-bash"}]])
site.main()
print(site.content)