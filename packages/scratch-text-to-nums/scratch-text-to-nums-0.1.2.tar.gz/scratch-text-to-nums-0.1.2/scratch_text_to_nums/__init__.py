__version__ = '0.1.2'

print('Scratch Encode/Decode Package By Joecooldoo\nScratchblocks: https://turbowarp.org/585257923/editor')

def split(word):
    return [char for char in word]

def encode(word): #This is for the custom command "encode"
  letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","0","_","-",".","!","?","@","#","$","%","^","&","*","(",")","+","=","{","}","|","[","]","","'","<",">","?",",",".","/"," ",";","\n",":","❌","✔",'️']

  #for index, item in enumerate(letters):
  #  if len(str(index)) == 1:
  #    print("0"+str(index))
  #  else:
  #    print(str(index))

  output = ""

  for i in split(word):
    if len(str(letters.index(i.lower()))) == 1:
      output = output + "0" + str(letters.index(i.lower())+1)
    else:
      output = output + str(letters.index(i.lower())+1)

  return(output)

def decode(word):
  letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","0","_","-",".","!","?","@","#","$","%","^","&","*","(",")","+","=","{","}","|","[","]","","'","<",">","?",",",".","/"," ",";","\n",":","❌","✔",'️']

  a_string = word

  split_strings = []
  n  = 2
  for index in range(0, len(str(a_string)), n):
    split_strings.append(a_string[index : index + n])

  go = 1

  result = ''

  for i in split_strings:
    result = result + letters[int(i) - 1]
  
  return(result)