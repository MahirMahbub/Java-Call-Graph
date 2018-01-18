def collectingPath(dir):
    count = 0
    for filename in os.listdir(dir):  # find file from the folder/dir(Recursively)
        pathway = os.path.join(dir, filename)  # making a string of path.
        if os.path.isfile(pathway) and pathway.endswith(".java"):  # checking for a file end with ".java"
            pathList.append(pathway)  # add the path of file in a list named "pathlist"
        elif os.path.isdir(pathway):  # if a folder/dir is found,access the
            collectingPath(pathway);  # Used recursive approach to find file from the directory as to the depth.
            # print("Collecting Path")
    for path in pathList:
        name = os.path.split(path)[1]  # seperating file name from path
        '''It is assured that a file should not contain more than one class and
        Class name and file name(eradicate .java part) are same.
        '''
        filename = name.split(".")[0]  # seperating class name from file name(example:file_name.java -->filename.(classname))
        classname.append(filename)  # add classname in a list named "classname"
    print(len(pathList))
def removeComments(string):
    string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all singleline comments (//COMMENT\n ) from string
    return string


def modification(path):
    """Modify text file and return the class body without start '{' and end '{'"""
    with open(path, 'rb') as f:  # opening the given file using path.
        data = f.read()  # reading raw data
        text = data.decode('utf-8')  # Decoding the data in a "file string" using utf-8 mode.

    with open('raw1.txt', 'wb') as f:  # writting back text to a temporary Simple text file.
        f.write(text.encode('utf-8'))

    text = open('raw1.txt', 'r+')  # opening the text file to modify the content for further use

    temp1 = text.read().replace("\n", "")  # Erasing newline feed/quotation.
    replacespace = re.compile(r'=')  # r'='Replacing two or more continuous space by a single space
    temp3 = replacespace.sub(' = ', temp1)
    replace = re.compile(r'\s\(')  # Replacing " (" with "("
    temp4 = replace.sub('(', temp3)
    replace = re.compile(r'\.')
    temp2 = replace.sub('.', temp4)
    replace = re.compile(r'\s+')
    temp6 = replace.sub(' ', temp2)  # Replacing "=" or " =" or "= " with " = "
    #temp5=removeComments(temp6)
    Inheritance= re.compile(r'extends\s*(\w+)\s*\{')
    InheritedClass=Inheritance.findall(temp6)
    #print(InheritedClass)
    if InheritedClass:
        global InheritedClassname
        InheritedClassname=InheritedClass[0]
        global InheritanceFound
        InheritanceFound=1
    leftindex = temp6.find("{");  # find first "{"
    rightindex = temp6.rfind("}");  # and last "}" for class body


    #print(temp5[leftindex + 1:rightindex])
    return temp6[leftindex + 1:rightindex]  # return class boby


def classAndObjectFunc(temp):
    """Collect Object and Classname in a pattern 'Classname.Object' name"""
    #ara2 = []
    #ara3 = []


    class_object = re.compile(r'(\w+)\s=\snew\s(\w+)\(')
    templist1 = class_object.findall(temp)   # find Object and corresponding Class from ...                                   #...pattern "Object = new Class()"
    #print(templist1)
    class_object = re.compile(r'(\w+)\s(\w+)\s=\snew\s(\w+)\(')#find Object and corresponding Class from...
                                                            #...pattern "Class1 Object = new Class()"
                                                            #...Class1 may be equal Class or not equal
    templist2 = class_object.findall(temp)
    #print("s")
    #print(templist2)
    #print(classname)
    for iterate in templist1:
        #print(iterate)
        if iterate[1] in classname:
            #print(iterate)
            ClassnameAndobjectname=iterate[1] + "." + iterate[0]
            if not ClassnameAndobjectname in ClassAndObject:
                ClassAndObject.append(ClassnameAndobjectname)
    #Add 'Classname.Object' in a list Class_And_Object
    #print(ClassAndObject)
    for iterate in templist2:
        if iterate[2] in classname:
            ClassnameAndobjectname = iterate[2] + "." + iterate[1]
            if not ClassnameAndobjectname in ClassAndObject:
                ClassAndObject.append(ClassnameAndobjectname)
    # Add 'Classname.Object' in a list Class_And_Object



def userDefinedFunctionSeperation(ClassName, temp):

    userFunction = re.compile(
        r'(public|protected|private|static|\s)+[\w\<[A-Za-z,\]*\>\[\]]*\s+(\w+) *\(([^\)]*)\) *(\({?|[^;])')
    #previously used REGEX1 with fault(public|private|protected)* (void|int|float|double|String|\w+)* (\w+)\(
    #previously used REGEX1 with fault(public|protected|private|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *(\{?|[^;])

    '''seperating userDefined functions in a list named "userdefined" '''
    ara = userFunction.findall(temp)
    print(ara)
    userdefined1=[]
    if ara:
        for i in ara:
            if i[-1]=="{" and (not i[-2]==""):
                Class_and_object_Recall(i[-2]) #Seperate "Class Object" passed as parameter as Class.Object at...
                                       #... list named "Class_and_objectFinal
    for i in range(len(ara)):
        # print(ara[i][-1])
        #if ara[i][-1] == "{" and not ara[i][-3] == 'main' and not ara[i][-3] == 'toString' and not ara[i][-3] == 'Main' :
        if ara[i][-1] == "{" :
            if not ara[i][-3] in javaKeyword:
            #Seperate Userdefined Function as Class.User_Defined_function at list named userdefined
                userdefined.append(ClassName + "." + ara[i][-3])


def Class_and_object_Recall(temp):
    #print(temp)
    if ',' in temp:
        #print(temp)
        templist =temp.split(',')

    elif len(temp)>1:
        templist=[temp]
    #spliting object and class name from user defined function parameter list
    #print(templist)
    for i in templist:
        if len(i.split(" "))>1 and not(i.split(" ")[-2]=="int" or i.split(" ")[-2]=="double"
               or i.split(" ")[-2]=="long" or i.split(" ")[-2]=="String[]"
               or i.split(" ")[-2]=="char"or i.split(" ")[-2]=="byte"
               or i.split(" ")[-2]=="short"or i.split(" ")[-2]=="float"
               or i.split(" ")[-2] == "Integer" or i.split(" ")[-2] == "Double"
               or i.split(" ")[-2] == "Long" or i.split(" ")[-2] == "Boolean"
               or i.split(" ")[-2] == "Char" or i.split(" ")[-2] == "Byte"
               or i.split(" ")[-2] == "Short" or i.split(" ")[-2] == "Float"
                                        or i.split(" ")[-2]=="boolean"):
            #if parameter contain primitive data type,ignore them.Otherwise add them in Class_And_ObjectFinal list
            if i.split(" ")[-2].lstrip(' \t\n\r') in classname:
                #print(i)
                ClassAndObject.append(i.split(" ")[-2]+"."+i.split(" ")[-1])
        else:
            pass
    #print(ClassAndObject)

def FunctionSeperation(temp,filename):
    #tempList = []
    replace = re.compile(r'\(')
    temp22 = replace.sub(' ( ', temp)
    # replace = re.compile(r'\.')
    # temp22 = replace.sub(' . ', temp)
    dictionary = {}
    #print(userdefined)
    for userfunc in userdefined: #iterate the "userdefined" (User Defined func name list)
        stack = []

        indexxpos = None
        if userfunc.split('.')[0] == filename:
            # print(userfunc.split('.')[0], filename)
            tempfuncname = ' ' + userfunc.split('.')[1] + ' ';
            # print(userfunc.split('.')[1])
        else:
            tempfuncname = "\0w017"
            continue
        try:
            indexxpos = temp22.index(tempfuncname)
        except ValueError:
            indexxpos = -1
        if indexxpos >= 0:
            lastindex = None
            firstindex = None
            while indexxpos < len(temp22):

                if temp22[indexxpos] == '{':
                    stack.append(['{', indexxpos])
                elif temp22[indexxpos] == '}':

                    if (len(stack) == 1):
                        lastindex = indexxpos
                        firstindex = stack[0][1]
                        #print(temp22[firstindex:lastindex+1])
                        dictionary[userfunc] = temp22[firstindex:lastindex+1]
                        break;
                    elif (len(stack) > 1):

                        stack.pop()
                    else:
                        pass
                indexxpos += 1

        else:
            pass
    #print(dictionary)


    ara11 = []
    dic = {}
    for key, funcbody in dictionary.items():
        object_used_when_called = []
        #print(key+ " : "+funcbody)
        calledFunction = re.compile(r'(\w+)\s*\.\s*(\w+)\s*\(')
        ara11 = calledFunction.findall(funcbody)
        #print(key)
        #print(ara11)
        #print(userdefined)
        for funcname in ara11:
            if funcname[0] == "super":
                tempList1.append(key + ':' + InheritedClassname + '.' + funcname[1])
            else:
                flago=0
                for tempo in ClassAndObject:
                    if (tempo.split(".")[1] == funcname[0]):
                        #print(funcname[1])
                        for userdef in userdefined:
                            if userdef.split('.')[-1] == funcname[-1]:
                                tempList1.append(key+ ':' + tempo.split(".")[0] + '.' + funcname[1])
                                flago=1
                                #print(key+ ':' + tempo.split(".")[0] + '.' + funcname[1])
                                break;

                            elif funcname[0] in classname:
                                tempList1.append(key + ':' + funcname[0] + '.' + funcname[1])
                                #Handling Inheritance
                                flago = 1
                                #print(key + ':' + funcname[0] + '.' + funcname[1])
                                break
                        if flago==1:
                            break

                    # Class+UserFunc()+Class(obj)+func()
        #print(key,tempList1)'''
        calledFunction2=re.compile(r' (\w+)\s*\(')
        ara22=calledFunction2.findall(funcbody)
        #print(key,ara22)

        for funcname in ara22:
            if funcname == "super" and InheritanceFound == 1:
                # print(ara22)
                tempList1.append(key + ':' + InheritedClassname + '.' + InheritedClassname)
            else:
                for userdef in userdefined:
                    if userdef.split('.')[1] == funcname and userdef.split('.')[0] == filename:
                        tempList1.append(key+ ':' +filename+ '.' + funcname)
                    # Class+UserFunc()+Class+func()
                    elif userdef.split('.')[1] == funcname:
                        tempList1.append(key + ':' + funcname + '.' + funcname)



    return tempList1

def BuildingMatrix(userdefined,CountedDictionary):
    userdefinedWithNoDuplicate = (userdefined)
    Matrix = [[0] * len( userdefinedWithNoDuplicate)for i in range(len( userdefinedWithNoDuplicate))]

    for key, value in CountedDictionary.items():
        for xindex,key1 in enumerate( userdefinedWithNoDuplicate):
            for yindex, key2 in enumerate( userdefinedWithNoDuplicate):
                if key1==key.split(":")[0] and key2==key.split(":")[1]:

                    Matrix[xindex][yindex]=value
    with open('file.txt', 'w') as f:
        for key1 in  userdefinedWithNoDuplicate:
            print("," + key1,end="", file=f)
        print(file=f)

        for i in range(len( userdefinedWithNoDuplicate)):
            print(str( userdefinedWithNoDuplicate[i]) + ",",end="", file=f)
            for j in range(len( userdefinedWithNoDuplicate)-1):
                print(str(Matrix[i][j])+",",end="", file=f)
            print(str(Matrix[i][len( userdefinedWithNoDuplicate)-1]),file=f)
def getvalue():
    global pathString
    pathString=entry.get()
    pattern=re.compile("^(?:[\w]\:|\\)(\\[a-z_\-\s0-9\.]+)+\.)")
    if pattern.match(pathString):
        root.destroy()
        return
    else:
        entry.delete(0,END)
        Label(text="*wrongpath",fg="Red").place(x=45,y=42)
def progressbar():
    try:
        root1 = Tk()
        root1.geometry("400x100+300+300")
        root1.resizable(width=False, height=False)
        root1.title("Processing")
        ttk.Label(text="Please Wait....").pack()
        progressbar = ttk.Progressbar(root1, orient=HORIZONTAL, length=250)
        progressbar.pack()
        progressbar.config(mode='indeterminate')
        progressbar.start()
        root1.mainloop()
    except:
        exit()

    #print(Matrix)

def askDirectory():

    root.foldername=filedialog.askdirectory()
    entry.insert(0,root.foldername)
    #getvalue()



if __name__ == "__main__":
    import os
    import _thread,time
    import re
    import json
    import pprint
    from collections import Counter
    from subprocess import Popen
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog
    import threading
    pathString=str()




    length = 0
    javaKeyword = ["catch", "continue", "for", "new", "switch", "default", "goto", "package", "synchronized", "do",
                   "if", "private", "this", "double", "implements", "protected", "throw", "else", "import", "public",
                   "throws", "enum", "instanceof", "return", "transient", "extends", "int", "short", "try", "final",
                   "interface", "static", "void", "finally", "long", "strictfp", "volatile", "float", "native","while"]

    pp = pprint.PrettyPrinter(indent=4)
    #FinalDic1 = {}
    #FinalDic2 = {}
    pathList = []
    #calledfunctionFinal = []
    #Class_And_Object = []
    classname = []
    ClassAndObject=[]
    userdefined = []
    #functionList = []
    tempList1 = []
    #Class_And_ObjectFinal = []

    try:
        root=Tk()
        message=None
        root.geometry("450x100+300+300")
        #root.iconbitmap(default='angry.ico')
        root.title("Call Graph Generator")
        root.resizable(width=False, height=False)
        ttk.Label(text="Path:").place(x=10,y=20)
        entry=ttk.Entry(root,width=50)
        entry.place(x=45,y=20)
        button=ttk.Button(root,text="Ok")
        button.place(x=180,y=70)
        button.config(command=getvalue)
        button = ttk.Button(root, text="Browse")
        button.place(x=360, y=18)
        button.config(command=askDirectory)
        if not message==None:
            entry.insert(0,message)

        root.mainloop()
        try:
            tthread1=_thread.start_new_thread(progressbar,())
        except:
            tthread1.join()
            exit()

        try:
            collectingPath(pathString)  # Collecting Path of all Java file
        except:
            exit()

        for path in pathList:
            name = os.path.split(path)[1]
            filename = name.split(".")[0]

            global Document
            Document = modification(path)
                #addlock=threading.lock()
            thread1 = threading.Thread(target=classAndObjectFunc, args=(Document,))
                #classAndObjectFunc(Document)
            thread2 = threading.Thread(target=userDefinedFunctionSeperation, args=(filename, Document,))
                #userdefined=userDefinedFunctionSeperation(filename, Document)
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()

        for path in pathList:
            global InheritanceFound
            InheritanceFound = 0
            global InheritedClassname
            InheritedClassname = ""
            name = os.path.split(path)[1]
            InheritanceFound=0
            filename = name.split(".")[0]
            Document = modification(path)
            #print(Document)

            fullList=FunctionSeperation(Document,filename)
            #print(fullList)
            #print(InheritanceFound)

        count = Counter(fullList)
        data=dict(count)
        BuildingMatrix(userdefined,data)
        #print(ClassAndObject)
        with open('Data.json', 'w') as f:
            json.dump(data, f)

        with open('Data.json', 'r') as f:
            download = json.load(f)
        #print(download)

        try:
            renamee = "file.txt"
            pre, ext = os.path.splitext(renamee)
            os.rename(renamee,"matrix"+ "." + "csv")
        except:
            os.remove("matrix.csv")
            renamee = "file.txt"
            pre, ext = os.path.splitext(renamee)
            os.rename(renamee, "matrix" + "." + "csv")
        os.remove("raw1.txt")
        p = Popen('matrix.csv', shell=True)
    except:
        exit()
    #print(userdefined)