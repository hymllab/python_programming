import requests
import xml.etree.ElementTree as ET


def crawling(limit):
    #ending of startPosition=4800 (1, 101, 201 ...)
    papers = {}
    titles = {}
    keywords = {}
    dois = {}
    key = '00000000'
    for i in range(limit) : #max: 48(TFSC) 14(UPAT)
        n = i*100+1
        #url = 'http://openapi.ndsl.kr/itemsearch.do?keyValue='+key+'&target=JAFO&searchField=SO&displayCount=100&startPosition=' + str(n) + '&sortby=pubyear&returnType=xml&responseGroup=simple&query=Technological%20forecasting%20and%20social%20change'
        url = 'http://openapi.ndsl.kr/itemsearch.do?keyValue='+key+'&target=UPAT&searchField=BI&displayCount=100&startPosition=' + str(n) + '&sortby=adate&returnType=xml&query=Artificial%20Intelligence'
        result = requests.get(url)
        root = ET.fromstring(result.text)
        outputRoot = root.find('outputData')

        for record in outputRoot.iter('record'):
            for articleTitle in record.iter('articleTitle'):
                print('TITLE:', articleTitle.text)
                title = articleTitle.text
            for abs in record.iter('abstract'):
                print('ABSTRACT:', abs.text)
                abstract = abs.text
            for y in record.iter('year'):
                print('year:', y.text)
                year = int(y.text)
            for k in record.iter('keyword'):
                print('keyword:', k.text)
                keyword = k.text
            for d in record.iter('doi'):
                print('doi:', d.text)
                doi = d.text
            print

            if year in papers.keys() :
                papers[year].append(abstract)
                titles[year].append(title)
                keywords[year].append(keyword)
                dois[year].append(doi)
            else :
                papers[year] = [abstract]
                titles[year] = [title]
                keywords[year] = [keyword]
                dois[year] = [doi]

    return papers, titles, keywords, dois


def crawling_patent(limit):
    #ending of startPosition=1400 (1, 101, 201 ...)
    ttcheck = {}
    abstracts = {}
    titles = {}
    ipcs = {}
    key = '00000000'
    for i in range(limit) : #max:  14(UPAT)
        n = i*100+1
        url = 'http://openapi.ndsl.kr/itemsearch.do?keyValue='+key+'&target=UPAT&searchField=BI&displayCount=100&startPosition=' + str(n) + '&sortby=adate&returnType=xml&query=Artificial%20Intelligence'
        result = requests.get(url)
        root = ET.fromstring(result.text)
        outputRoot = root.find('outputData')

        for record in outputRoot.iter('record'):
            for patentTitle in record.iter('patentTitle'):
                print('TITLE:', patentTitle.text)
                title = patentTitle.text
            for abs in record.iter('abstract'):
                print('ABSTRACT:', abs.text)
                abstract = abs.text
            for date in record.iter('applicationDate'):
                print('applicationDate:', date.text)
                dt = int(date.text)
                year = int(date.text[:4])
            for d in record.iter('ipc'):
                print('ipc:', d.text)
                ipc = d.text
            print

            if (title.lower() not in ttcheck.keys()) and (abstract) :
                if year in abstracts.keys() :
                    abstracts[year].append(abstract)
                    titles[year].append(title)
                    ipcs[year].append(ipc)
                else :
                    abstracts[year] = [abstract]
                    titles[year] = [title]
                    ipcs[year] = [ipc]
                ttcheck[title.lower()] = 1

    return abstracts, titles, ipcs


def fullArticles(doidata):
    '''
    extract full articles using Elsevier API
    :param doidata:
    :return: list of artcle contents
    '''
    result = []
    key = ''
    for doi in doidata:
        if doi:
            print(doi)
            doi = doi[18:]
            url = 'http://api.elsevier.com/content/article/doi/' + doi + '?APIKey='+key+'&httpAccept=text/xml'
            r = requests.get(url)
            with open('./data/' + doi.replace('/', 'slash') + '.xml', 'w') as f: f.write(r.text)
            result.append(r)

    return result


