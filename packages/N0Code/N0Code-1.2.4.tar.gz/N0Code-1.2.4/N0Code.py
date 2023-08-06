#coding=utf-8
from genericpath import exists
from requests.models import Response
from problem import *
from user import *
import argparse
import os
import json
import re
from i18n import I18n
import i18n
def consoleOut(identity,content):
    print("[%s]:%s"%(identity,content))
try:
    from lxml.html import etree
except:
    consoleOut("N0Code",I18n("Please run 'pip install lxml"))
    exit(0)
import sys
class Question:
    def __init__(self,id,title,slug,hide,acs,submit,difficulty) :
        self.id=id
        self.title=title
        self.slug=slug
        self.hide=hide
        self.acs=acs
        self.submit=submit
        self.difficulty=difficulty
class Answer:
    def __init__(self,title,Description,author):
        self.Title=title
        self.Description=Description
        self.Author=author
    Challenges=[]
    Responses=[]
    def set(self,response,**kwargs):
        self.Challenges.append(kwargs)
        self.Responses.append(response)
    
    def check(self,expFunc):
        correct=0
        wrong=0
        print("\n["+self.Title+"]")
        print('"'+self.Description+'"\n')

        for challengeId in range(0,len(self.Challenges)):
            challenge=self.Challenges[challengeId]
            #print(challenge)
            try:
                res=expFunc(**challenge)
            except Exception as e:
                print(I18n("Do not specify a parameter name."))
            if res==self.Responses[challengeId]:
                print("[Correct]:%s --> %s" % (challenge,res))
                correct+=1
            else:
                print("[Wrong]:%s --> %s Answer: %s" % (challenge,res,self.Responses[challengeId]))
                wrong+=1
        print("\nCorrect: %s/%s" % (correct,len(self.Challenges)))
        print("Wrong: %s/%s" % (wrong,len(self.Challenges)))
        if wrong==0:
            print(I18n("\nThis Challenge Has Been Solved By ")+self.Author)
        else:
            print("\n"+self.Author+I18n("! Try again!"))
replaceList={
    "<p>":"",
    "</p>":"",
    "<code>":"",
    "</code>":"",
    "<strong>":"",
    "</strong>":"",
    "<em>":"",
    "</em>":""
}
def esc(targetStr,escList='$n0p'):
    if escList=='$n0p':
        specialChar=['$','(',')','*','+','.','[',']','?','^','\\','{','}','|']
    else:
        specialChar=escList
    targetStr=list(targetStr)
    index=0
    SKIP=False
    for char in targetStr:
        if not SKIP:
            if char in specialChar:
                targetStr.insert(index,'\\')
                SKIP=True
        else:
            SKIP=False
        index+=1
    retStr=''
    for i in targetStr:
        retStr+=i
    return retStr
def match(left,right,targetStr,onlyContent=True):
    matchLeft=esc(left)#正则特殊字符加反斜杠
    matchRight=esc(right)
    flags=[]
    while True:
        reFlag=re.search(matchLeft+".+?"+matchRight,targetStr)
        try:
            findFlag=reFlag.group(0)
            if onlyContent:
                flags.append(findFlag[len(left):0-len(right)])
            else:
                flags.append(findFlag)
            targetStr=targetStr.replace(findFlag,'',1)
        except:
            break
    return flags

def Xpath(target,xpath):
    contentHtml=etree.HTML(target)
    content=contentHtml.xpath(xpath)
    result=[]
    for i in content:
        string=etree.tostring(i,encoding = "utf-8", pretty_print = True, method = "html")
        result.append(string.decode("utf-8"))
    return result
def getQuestion(id):
    id=int(id)
    url = "https://leetcode-cn.com/api/problems/all/"
    headers = {"Content-Type": "application/json"}
    r = requests.get(url, headers=headers)
    jsonData = r.json()
    for question in jsonData["stat_status_pairs"]:
        questionData=question["stat"]
        if questionData["question_id"]==id:
            result=Question(
                questionData["question_id"],
                questionData["question__title"],
                questionData["question__title_slug"],
                questionData["question__hide"],
                questionData["total_acs"],
                questionData["total_submitted"],
                -1
                )
            return result
    return None
def getMaxQueue():
    url = "https://leetcode-cn.com/api/problems/all/"
    headers = {"Content-Type": "application/json"}
    r = requests.get(url, headers=headers)
    jsonData = r.json()
    ids=[]
    for question in jsonData["stat_status_pairs"]:
        questionData=question["stat"]
        ids.append(questionData["question_id"])
    ids.sort()
    return ids
def divide(string,split):
    parts=string.split(split)
    try:
        return parts[0],split.join(parts[1:])
    except:
        return parts[0],None
def getArgv(argv,id,default):
    try:
        return argv[id]
    except:
        return default
SetTestCode='\nAns.set({resp},{chal}){anno}'
StdCode='''#coding=utf-8
#Question Id: {QuestionId}
import N0Code
{DefaultCode}
        return

Ans=N0Code.Answer("{Title}","{Description}","{Author}")'''       
def new(questionId=-1):
    if questionId==-1:
        questionId=args.questionId
    if args.author==None:
        author=Config["Author"]
    else:
        author=args.author
    if questionId==None:
        print(I18n("Lack of parameter")+" 'QuestionId'")
        return
    try:
        questionId=int(questionId)
    except:
        consoleOut(I18n("Error"),I18n("Question Id must be an integer."))
        return
    consoleOut(I18n("QuestionId"),questionId)
    question=getQuestion(questionId)
    if question!=None:
        problemInfo=get_problem_info(question.slug)
        if i18n.Language=="Zh_cn":
            title=problemInfo["translatedTitle"]
            contentRaw=problemInfo["translatedContent"]
        else:
            title=problemInfo["title"]
            contentRaw=problemInfo["content"]
        consoleOut(I18n("Title"),title)
        slug=problemInfo["titleSlug"]
        consoleOut(I18n("Slug"),slug)
        content=Xpath(contentRaw,"//p")[0]
        for i in replaceList:
            content=content.replace(i,replaceList[i])
        consoleOut(I18n("Description"),content)
        code=None
        for lang in problemInfo["codeSnippets"]:
            if lang["langSlug"]=="python":
                code=lang["code"]
                break
        if code==None:
            consoleOut(I18n("Notice"),I18n("This problem does not support using python"))
        else:
            rubbish,code=divide(code,"\n    ")#去Solution类
            funcName=match("def ","(",code)[0]
            fp = open(title+".py",'w',encoding='utf-8')
            writeCode=StdCode.format(
                QuestionId=questionId,
                DefaultCode=code,
                Title=title,
                Description=content.replace("\n",""),
                Author=author
                )
            writeCode=writeCode.replace("self, ","")
            #print(contentRaw)
            tests=Xpath(contentRaw,"//pre")
            for test in tests:
                anno=""
                test=test.replace("\n","")
                #print(test)
                result= match("</strong>","<strong>",test)
                if len(result)<1:
                    continue
                challenge=result[0]
                if len(result)<2:
                    result= match("</strong>","</pre>",test.replace("</strong>","",test.count("</strong>")-1))
                    response=result[0]
                else:#有注释
                    response=result[1]
                    anno=match("</strong>","</pre>",test.replace("</strong>","",test.count("</strong>")-1))[0]
                if anno!="":
                    anno="#"+anno
                consoleOut(I18n("Example"),challenge+" --> "+response)
                writeCode+=SetTestCode.format(resp=response,chal=challenge,anno=anno)
            writeCode+="\nAns.check({0})\n".format(funcName)
            fp.write(writeCode)
            Config["_LastQuestion"]=questionId
            saveConfig()
            return True
    else:
        print(I18n("Problem not found."))
        return False
Config={
    "Author":"Unknow",
    "_QuestionStatus":{

    },
    "_Now":1,
    "User":"",
    "Password":"",
    "_LastQuestion":0,
    "Language":"En"
}
def saveConfig():
    try:
        with open('.nocode', 'w',encoding="utf-8") as f:
            f.write(json.dumps(Config))
        return True
    except Exception as e:
        consoleOut("Error",str(e))
        return False
def initWorkSpace():
    if os.path.isfile(".nocode"):
        consoleOut(I18n("Notice"),I18n("The current folder is already a N0Code-workspace."))
    else:
        if saveConfig():
            consoleOut("OK",I18n("Initialization is complete.Enjoy your algorithm :)"))
def setConfig():
    try:
        setting=sys.argv[2]
    except Exception as e:
        print("Usage: N0Code.py set Author=N0P3")
        return
    param,value=divide(setting,"=")
    if len(param)>0 and param[0]!="_":
        if param in Config:
            Config[param]=value
            if saveConfig():
                print("OK")
        else:
            print(param+I18n(" Not Found."))
    else:
        print(param+I18n(" Can't be accessed."))
def next():
    queue=getMaxQueue()
    try:
        questionId=queue[queue.index(Config["_LastQuestion"])+1]
        if not new(questionId):
            consoleOut(I18n("Error"),"Next error.")
    except Exception as e:
        print(I18n("Congratulations! You have already finished all the questions.")+str(e))
functions={
    "init":initWorkSpace,
    "new":new,
    "set":setConfig,
    "next":next
}
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="For LeetCode,For Dream.\nDeveloped by N0P3.")
    parser.add_argument("option",choices=functions.keys(),help=I18n("Option."))
    parser.add_argument("questionId",nargs='?',help=I18n("Question Id."))
    parser.add_argument("author",nargs='?',help=I18n("Author."))
    parser.add_argument("-l", "--language", help=I18n("Set language."),default="Default",choices=list(i18n.texts.keys()).append("En"))
    args = parser.parse_args()
    i18n.Language=args.language
    if os.path.isfile('.nocode'):
        with open(".nocode","r") as f:
            Config=json.loads(f.read())
        if args.language=="Default":
            i18n.Language=Config["Language"]
    elif args.option=="init":
        pass
    else:
        consoleOut(I18n("Error"),I18n("The current folder is not a N0Code-workspace.Please run 'N0Code.py init'."))
        sys.exit(0)
    
    
    functions[args.option]()