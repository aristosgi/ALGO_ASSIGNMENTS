import pprint
import sre_yield
import time
import argparse
import string

parser = argparse.ArgumentParser()
parser.add_argument("csv_file")
parser.add_argument("txt_file")
args = parser.parse_args()
csv_file = args.csv_file
txt_file = args.txt_file


expressions = {}
graph = {}
reqular_expressions = {}
regular = {}

with open(txt_file) as text:
    content = text.read()
    reg_ex = list(content.splitlines())

with open(csv_file)as file:
    for row in file:
        nodes = [x for x in row.split(',')]
        graph[nodes[0]] = []
        for i in range(len(nodes)):
            graph[nodes[0]].append(nodes[i])        
    file.close
words_dots = {}
for row in graph:
    words_dots[row] = []
    words_dots[row].append(graph[row][1])
    if("." not in graph[row][1]):
        expressions[row] = graph[row][1]

def find_not_solved():
    not_solved = []
    dots = []
    known = []
    for row in graph:
        c1=0
        c = 0
        for col in graph[row]:
            c = c + 1        
            if(c==2):
                if("." in col):
                    not_solved.append(row)
    return not_solved
    
def fill_gaps():
    
    for row in graph:
        words = []
        places = []
        if("." not in graph[row][1]):
            for i in range(2 , len(graph[row])):
                if(i % 2 == 0):               
                    word = graph[row][i]
                else:
                    place = graph[row][i]
                    for j in range(2 , len(graph[word]) , 2):
                        a = graph[word][j]
                        if(a == row):
                            help = j 
                            break
                    np = graph[word][help+1]
                    letter = graph[row][1][int(np)]
                    old_string = graph[word][1]
                    string = [car for car in old_string]
                    string[int(place)] = letter
                    graph[word][1] = "".join(string) 
                   

def find_known_letters():
    known = []
    for col in not_solved:
        count1 = 0
        if ("." in graph[col][1]):
            for car in graph[col][1]:
                if(car != "."):
                    count1 = count1 + 1                   
            known.append(count1 / len(graph[col][1]))          
    return known


def find_reg(word):
    exp = []
    places = []
    letters = []
    length = len(word)
    for car in word:
        if(car != "."):
            places.append(word.index(car))
            letters.append(car)
    for row in reg_ex:
        ex_list = list(sre_yield.AllStrings(row , max_count=5 , charset=string.ascii_uppercase))
        for ex in ex_list:
            
            if(len(ex) == length):
                c5 = 0

                for i in range(len(letters)):
                    if(ex[places[i]] == word[places[i]]):
                        c5 = c5 + 1
                    if(c5 == len(letters)):
                        exp.append(row)
                if(len(letters) == 0):
                    exp.append(row)
                    break
    return exp

def is_solved():
    flag = True
    for row in graph:
        if("." in graph[row][1]):
            flag = False
    return flag    

def find_per():
    per = []
    for i in range(len(known)):
        per.append(known[i] / unknown[i])
    return per

def listToString(s): 
    str1 = "" 
    for ele in s: 
        str1 += ele 
    return str1 

def correct_word(exp , word):
    listt = list(sre_yield.AllStrings(exp , max_count=5 , charset=string.ascii_uppercase))
    places = []
    letters = []
    length = len(word)
    cw = []
    for car in word:
        if(car != "."):
            places.append(word.index(car))
            letters.append(car)
    
    for row in listt:
        if(len(word) == len(row)):
            if(len(letters)==0):
                cw.append(row)
        if(length ==  len(row)):
            c5 = 0
            for i in range(len(letters)):
                if(row[places[i]] == word[places[i]]):
                    c5 = c5+1
                if(c5 == len(letters)):
                    cw.append(row)
    return cw
to_solve = []
def word_to_solved():
    fill_gaps()
    known = find_known_letters()
    not_solved = find_not_solved()
    if(len(not_solved)>0):
        a = known.index(max(known))
        b = not_solved[a]
        if(b not in to_solve):
            to_solve.append(b)
    else:
        to_solve.append(not_solved[0])

def validWord(row1):
    f = False
    a = (to_solve[row1]) 
    word = graph[a][1]
    exp = find_reg(word)
    for ex in exp:
        if(dict[ex] == True):
            f = True
    return f
found = []
def solve(row1):
    cw = []
    a = (to_solve[row1])
    word = graph[a][1]
    exp = find_reg(word) 
    
    for ex in exp:
        if(ex not in found):
            cw1 = correct_word(ex , word)
            for w in cw1:
                found.append(ex)
                graph[a][1] = w
                expressions[a] = ex
                fill_gaps()
                known = find_known_letters()
                not_solved = find_not_solved()
                if(len(not_solved)!= 0):
                    word_to_solved()
                if(is_solved()):
                    for i in range(len(expressions)):                       
                        print(i , expressions[str(i)] , graph[str(i)][1])
                    return True
                if(solve(row1+1)):
                    return(True)
                graph[a][1] = listToString(words_dots[a])
                found.remove(ex)
    
fill_gaps()
not_solved = find_not_solved()
known = find_known_letters()
word_to_solved()
solve(0)

