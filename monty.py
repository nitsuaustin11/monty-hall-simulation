from random import choice
import csv
from copy import copy

#to run this program simply write in the console >>> python monty.py
#it will prompt you with inputs to run the simulation.

#***********************************************************
#DO NOT RUN THE PROGRAM WITH EXCEL OPEN, IT WILL NOT WORK!.
#**************************************************************

#this is usefull for creating a multiple choice question of any length.
def get_uniqe_list(L): #this is called a function decloration, this declares a function. => look up functions and paramaters to understand more
  """returns a list of unique options to a lenght of a number ex => get_unique(5) returns 
      [a1,a2,a3,a4,a5]"""
  ret_lis = [] #we need to initalize an empty list here, youll see this alot, this is because we cant use things that dont exist yet.
  for i in range(L):  #classic for loop. this will loop through a length of "L" times whatever L is.
    user_hex = hex(i)[2:] # this creates a cool unique number in hex code, 1 looks like "1" but "10" is a and 64 is something like a2
    # anyway, this is usefull for getting a list of uniqe items for each number of "L".
    ret_lis.append("a"+user_hex) #we are just putting our unique item in the list we innitalized.
  return ret_lis #then when its all done, we return it. => i would recomend looking up difference of return and print in python.

#i would challenge you to make a function that can take a number as a paramater and will return a new list of that lenght.
#do this challenge on your own after you feel like you understand this function.


#this is a very similar senario as our first function, however, were just going to retun random options in a list from the list of options.
def rand_list(qty,options):
  """creates a random list of length n, using only options from a given list. 
      rand_list(5,[a,b,c]) -> [a,b,a,c,b]"""
  li_ans = []
  for i in range(qty): #we want the list to be as long as the amount of questions in the "test", so qty will usually be the number of questions in a test
    winner = choice(options) #gets our random option.
    li_ans.append(winner) #appends to list
  return li_ans

#understanding how to describe a type of list can be usefull, i would recomend figuring out how to make various list now that you know how
#to make a list of length X. for a challenge pick a random pattern like count by 2, or count by N. the number could be "2", "3", "4" and return a list of length 10 counting up by that number
#so, for example CountByN(4) => would return [4,8,12,16,20,24,28,32,36,40]. figure out how to make this.
#another unique list could instead flip a list backwards. if were given a list [a,b,c,d,e], the new list would be [e,d,c,b,a] - this is a difficult problem but if your up to it id try it.

def get_rand(options, exclude):
  """returns a random item from a list, but can exclude options from that list via an exclude list"""
  return choice([ans for ans in options if ans not in exclude]) 

#this list takes alot of paramaters as you can see. but fundamentally, im just returning a new list like normal. yo can quickly tell by looking at what the function is returning.
def probable_lis(leng:int,opt:list,ans:list,gues:list,elim:list) -> list:
  """this will eliminate options from a list depending on the desired amount of items to eliminate
    very similar to the previous function"""
  ret_lis = []
  for i in range(leng): # itterating through a list of length N... 
    jo = copy(opt) #this is interesting, but dont worry about it. here im creating my variable jo, which is equal to the options given. 
    exclude = [ans[i], gues[i]] # list of items to exclude. could be [a,b]

    for j in range(len(opt)-(len(opt)-elim)): #this is a new concept that also becomes really usefule. its called nesting. you can see its a forloop inside a forloop. 
      #i would recomend looking up nested forloops to understand the concept better.
      rem_ind = get_rand(jo,exclude)
      jo.remove(rem_ind)
    ret_lis.append(jo)
  return ret_lis

#for a challenge you should make a function that utilizes nested for loops. this is usefull for manipulating list inside list ex =>  [[a,b,c,d,e],[a1,a2,a3,a4,a5],[a2,b2,c2,d2,e2]]
#start by just returning the first item in each list for example if our input was the example i gave. the new function would return, [a,a1,a2]. 
#using nested forloops is the best solution for this.


def switch(leng,u_ans,out_lis):
  """this function will switch your answer to another option in the list provided. your odds go up the less items in this list"""
  new_lis = []
  for i in range(leng):
    out_lis[i].remove(u_ans[i]) #removes the users guess from the options
    jo = choice(out_lis[i])
    new_lis.append(jo) #appends the new answer to the list and returns it
  return new_lis

def compare(a,b,leng):
  """compares two list, the list that is correct, and a users guesses if your answers are correct
  correct goes up one point."""
  win = []
  correct = 0
  incorrect = 0
  for i in range(leng):
    if a[i] == b[i]:
      correct += 1 
      win.append("Won")
    else:
      win.append("lost")
      incorrect += 1
  return [correct, win]


#youll notice below that i finally use all the functions i created above to smoothly and neatly run the program. 
def main():
  """runs the whole program simulating your random answers and guesses for hundreds of questions, takes input and will return answers to the terminal, aswell as in a csv file"""
  length = 1000 #add int(input(""))
  possible_answers = int(input("how many possible answers: "))
  list_of_options = get_uniqe_list(possible_answers)

  print("your possible answers", possible_answers, list_of_options)

  elim_W_Certanty = int(input("how many answers can you eliminate with certanty: "))
  if elim_W_Certanty > possible_answers -2: #here we just want to check that were not eliminating more answers in a question that there are answers to eliminate. - we dont want to eliminate our answer and the answer.
    elim_W_Certanty = possible_answers - 3

  answers = rand_list(length,list_of_options) #the holy grail = the "true" answers to the test!
  guesses = rand_list(length,list_of_options) #your shitty guesses

  result_elim_max = probable_lis(length,list_of_options,answers,guesses,(possible_answers-2))#a list of items where we eliminated all other options
  result_elim_some = probable_lis(length,list_of_options,answers,guesses,elim_W_Certanty)#a list where we elimintated only a few answers

  guess_w_switch = switch(length, guesses, result_elim_max) #switching to options in the remaining options list
  guess_elim_some = switch(length, guesses, result_elim_some)#switching to options in the remaining options list

  first_score = compare(answers, guesses,length) #compares what you would have got without switching

  second_score = compare(answers, guess_w_switch,length) #compares what you would get via eliminating max options.

  third_score = compare(answers, guess_elim_some,length) #compares what your score would be if you only could eliminate a certian number of options

  print("score without switching", first_score[0]/10,"%")
  print("score from switching under best conditions:", second_score[0]/10,"%")
  print(f"score from eliminating {elim_W_Certanty} and switching: ", third_score[0]/10,"%")

  #this is where we write to a csv file. just look up "reading and writing to files in python",
  with open("monty.csv", "w", newline="") as file:
    writer = csv.writer(file,)
    writer.writerow(["Stay score",first_score[0], "expected probability", f"{100/possible_answers}%"])
    writer.writerow(["Switch score", second_score[0],"expected probability", f"{(100-100/possible_answers)}%"])
    writer.writerow(["Elim Some options", third_score[0],"expected probability", f"{100/(possible_answers-elim_W_Certanty-1)}%"])
    writer.writerow(["number of options", possible_answers])
    writer.writerow(["Answers eliminated with certanty", elim_W_Certanty])
    writer.writerow(["Possible Answers", list_of_options])

    writer.writerow(["Total Questions",length])
    writer.writerow(["Answers", "innital Guess", "Switched Guess", "Eliminated with Certanty", "Stay Result","switched result", "ratio of elim"])
    for i in range(length):
      writer.writerow([answers[i], guesses[i], guess_w_switch[i],guess_elim_some[i]  ,f"Switch -{second_score[1][i]}",f"Stay -{first_score[1][i]}", f" elim {elim_W_Certanty} and Switch-{third_score[1][i]}"])

if __name__ == "__main__": #this is a little thing that is called "good practice". basically it just runs the main function if i type "python monty.py" in the terminal. 
  #however if i were to call this file from another file i dont want it to run the program. because in that case im probably just using the functions i made in this file not trying to run a simulation.
  main()