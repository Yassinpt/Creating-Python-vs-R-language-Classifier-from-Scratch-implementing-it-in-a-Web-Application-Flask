# Beautiful Soup is a Python package for parsing HTML and XML documents.
# It creates a parse tree for parsed pages that can be used to extract data from HTML,
# which is useful for web scraping. It is available for Python 2.7 and Python 3.

import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString
from csv import writer
from time import sleep


# Nous allons balayer 23532 pages dans stackOverFlow Pour le sujet Python
def getQuestionsUrlsPage(pageNumber):
    questionsUrls = []
    url = "https://stackoverflow.com/questions/tagged/r?sort=newest&page={}&pagesize=30".format(pageNumber)

    response = requests.get(url)
    if (response != None):

        soup = BeautifulSoup(response.text, 'html.parser')
        questions = soup.find(id="questions")

        # Question.contents contient les (antislash) n : retour à la ligne dans chaque position 0,2,4 .. et a la fin de 1 jusqu a 99

        questionsDiv = questions.find_all(class_="question-summary")
        for questionDiv in questionsDiv:
            divWhoHasUrl = questionDiv.contents[
                3]  # divwhoHasUrl c est le div qui contion le lien de question dans une balise h3; la premiere balise
            hTagWhoHasUrl = divWhoHasUrl.contents[
                1]  # hTagWhoHasUrl c est la balise h3 qui contient le lien hypertexte vers les questions
            aTagWhoHasUrl = hTagWhoHasUrl.contents[
                0]  # aTagWhoHasUrl c est la balise a qui contint le link vers les questions dans un attribut href
            print(aTagWhoHasUrl)
            try:
                url = aTagWhoHasUrl.get('href')  # la methode het permet de récupérer le lien dans href pour la balise a
                questionsUrls.append(url)
            except:
                getQuestionsUrlsPage(pageNumber + 1)
        return questionsUrls

    else:
        sleep(600)
        getQuestionsUrlsPage(pageNumber)


# a ce stade on est arrivé a avoir les liens de tous les urls vers chaque question dans tous les pages 23532  dans la liste questionsUrls gener par la recherche dans le site avec le mot clé python

# exemple questionsUrls[0]="/questions/56319401/how-to-implement-user-input-on-a-website-to-go-to-specific-site-for-scrapping"


# dans cette partie on va accéder à chaque url pour récupérer le texte de chaque question
def writePosts(questionsUrls, fileName):
    sitePrefix = "https://stackoverflow.com"
    questionsFullUrls = [sitePrefix + questionsUrl for questionsUrl in questionsUrls]
    with open(fileName, "w", encoding="utf-8") as csv_python:  # ecrire chaque post dans un fichir csv
        csv_writer = writer(csv_python)
        headers = ["post", "python or r"]
        csv_writer.writerow(headers)  # on écrit les headers dans le fichier Python_Posts.csv
        for fullUrl in questionsFullUrls:
            try:
                rsp = requests.get(fullUrl)
                if (rsp == None):
                    sleep(600)
                else:
                    sp = soup = BeautifulSoup(rsp.text, 'html.parser')
                    posts = soup.find(class_="post-text")
                    paragraphs = posts.find_all('p')
                    post = ""
                    for paragraph in paragraphs:
                        post = post + '' + paragraph.get_text().replace("\n",
                                                                        "")  # avec get_text() on récupere le contenu de chaque balise p
                    postLabaled = [post, "r"]
                    csv_writer.writerow(postLabaled)
            except :
                pass


# Ici on va faire un script pour environ 1000 pages on on va faire un retard de 5 min soit 300 sec pour que le site ne bloque pas notre adresse ip
# dans la premiere étape on commence par startPage=1 c est dire la premiere page et finishPage=20
# on onvoye maximum 30 requets per sec pour que la requete ne soit pas bloqué par le site stackoverflow
for i in range(564,565):
    questionsUrls = getQuestionsUrlsPage(i)
    nameFile = "Posts_R_Page" + "_" + str(i) + ".csv"

    writePosts(questionsUrls, nameFile)
    sleep(5)

