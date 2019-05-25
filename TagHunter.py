# -*- coding: utf-8 -*-
"""TCC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yhYgEBFBEDGmrnUFXyZ_DSSO3RWakKPG
"""

from bs4 import BeautifulSoup
import requests
import json
import datetime
import pymysql
import threading
import random
"""
TAG HUNTER
@params str url
@params str sitename
@params list tagContent[[str(tag), dict(features), (optional)str(parameter to get the content)], [str(tag), dict(features), (optional)str(parameter to get the content)], [str(tag), dict(features), (optional)str(parameter to get the content)]]
"""

class TagHunter:
  
  def __init__(self, url, sitename, tagContent):
    self.sitename = sitename
    self.url = []
    self.urlInicial = url
    self.forUrls = []
    
    self.tagContent = tagContent
    self.url.append(url)
    self.pages = []
    self.content = []
    self.dirtyContent = []
    self.urls_ja_escaneadas = []
    self.confirmPage = True
    self.confirmAnalyze = True
    self.confirmUrls = True
    self.main()

  def main(self):
    while self.confirmPage == True or self.confirmAnalyze == True:
      
      t1 = threading.Thread(target=self.GetPages)
      t2 = threading.Thread(target=self.GetPages)
      t3 = threading.Thread(target=self.Analyze)
      t1.start()
      t2.start()
      t3.start()
      print(len(self.url))
      t1.join()
      t2.join()
      
    t3.join()
    self.confirmClean = self.CleanContent()
    
  def Analyze(self):
    try:
      if len(self.pages) != 0:
        pageForAnalyze = self.pages.pop()
        
      else:
        return False 
      
      page = pageForAnalyze[1]
      tempContent = []
   
      for z in self.tagContent:  
        result = page.find_all(z[0])
        
        for y in result:
          tempContent.append(y)
      
      result= [pageForAnalyze[0], tempContent]
      self.dirtyContent.append(result)
    except KeyError:
      return False
      
    else:
      return True
      
  def CleanContent(self):
    while True:
     
      try:
        
        for x in self.tagContent:
          
          for key,val in x[1].items():
            tempContent = []
            result = []
            for y in self.dirtyContent:
              
              for z in y[1]:
                
                if z.get(key) != None:
                  if val in z.get(key):      
                    tempContent.append(z)
                
              temploc = [y[0], tempContent]
              if temploc not in result:
                result.append(temploc)
              
          if len(x) == 3:  
            for x in len(0, result):
              for z in range(0, len(result[x][1])):
                result[x][1].append(result[x][1][z].get(x[2]))
          
        self.content.append(result)

        return True
      except KeyError:
        return False
      
      else:
        pass
    
    return True

  def GetPages(self):
    try:
      tempUrl = []
      tempPages = []
      nUrl = len(self.url)
      if nUrl != 0:
        if nUrl != 1:
          tempUrl = self.url.pop(random.randrange(0, nUrl))
        else:
          tempUrl = self.url.pop()
      else:
        self.confirmPage =  False
      tempPages = []
      if tempUrl not in self.urls_ja_escaneadas:
          self.urls_ja_escaneadas.append(tempUrl)
          resposta = requests.get(tempUrl)
          
          if resposta.status_code == 200:
            tempPages.append(tempUrl)
            tempPages.append(BeautifulSoup(resposta.content, "html.parser"))
          
            self.pages.append(tempPages)
            self.url = list(set(self.url))
            bs = BeautifulSoup(resposta.content, "html.parser")
            links = bs.find_all('a')
            links = list(set(links))     
            for link in links:
              
              if link["href"].startswith(self.urlInicial) and link["href"] not in self.urls_ja_escaneadas and link["href"] not in self.urls_ja_escaneadas and ".html" not in tempUrl and ".php" not in tempUrl:
                self.url.append(link["href"])
              
              elif link["href"].startswith("/") and tempUrl+link["href"] != tempUrl+"/" and tempUrl+link["href"] not in self.urls_ja_escaneadas and link["href"] not in self.urls_ja_escaneadas and ".html" not in tempUrl and ".php" not in tempUrl:
                self.url.append(tempUrl + link["href"])
                
              elif link["href"].startswith(tempUrl) and tempUrl+link["href"] != tempUrl+"/" and link["href"] not in self.urls_ja_escaneadas and link["href"] not in self.urls_ja_escaneadas and ".html" not in tempUrl and ".php" not in tempUrl:
                self.url.append(link["href"])
            self.confirmPage = True
    except KeyError:
      self.confirmPage = False    


queue = [["https://araquari.ifc.edu.br/","araquari.ifc",[["div", {"class":"page-subheader"}]]], ["https://ctf-br.org","ctf-br.org",[["h1",{"h1":"page-introduce-title"}]]]]    


print(TagHunter("https://araquari.ifc.edu.br/","araquari.ifc",[["div", {"class":"page-subheader"}]]).content)

