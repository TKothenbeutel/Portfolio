import shutil
import textwrap
import builtins

from pyscript.js_modules import settings # type: ignore

def bold(s:str)->str:
  """Formats to bold given string when printed in console"""
  ###Look into blessed to make UI a bit more pretty (may need big overhaul...)
  return f'\u001b[1m{s}\u001b[0m'

def underline(s:str)->str:
  """Formats to underline given string when printed in console. Note: only letters can be underlined"""
  return '\u0332'.join(s + ' ')[:-1]


def wrap_text_to_terminal(text: str) -> str:
    """Wraps text to the current terminal width using textwrap."""
    width = settings.getCols()

    splittedText = text.splitlines()

    """
    #Temp remove bold
    specialCharIndices = [] #True = bold; False = underline
    boldEnd = True
    for i in range(len(splittedText)):
      chunk = splittedText[i]
      specialCharIndices.append([])
      index = len(chunk)-1
      while('\u001b' in chunk or '\u0332' in chunk):
        if(chunk[index] == '\u001b'):
          #Add bold spot to list
          specialCharIndices[-1].append((index,True))
          #Remove bold
          res = chunk.rsplit('\u001b[0m',1) if boldEnd else chunk.rsplit('\u001b[1m',1)
          #Update variables
          splittedText[i] = res[0] + res[1]
          chunk = splittedText[i]
          boldEnd = not boldEnd
        elif(chunk[index] == '\u0332'):
          #Add underline to list
          specialCharIndices[-1].append((index,False))
          #Remove underline
          res = chunk.rsplit('\u0332',1)
          #Update variables
          splittedText[i] = res[0] + res[1]
          chunk = splittedText[i]
        index -= 1
    """

    wrapped_lines = [textwrap.fill(line,width=width, drop_whitespace=False, replace_whitespace=False) for line in splittedText]
    """
    #Add in bold
    boldEnd = False
    for i in range(len(wrapped_lines)):
      for charIndex in reversed(specialCharIndices[i]):
        pos = 0
        for j in range(len(wrapped_lines[i])+1):
          if(pos == charIndex[0]):
            if(charIndex[1]):
              #Ensure \n isn't in the way
              if(j < len(wrapped_lines[i])-1 and wrapped_lines[i][j] == '\n'):
                j = j-1 if boldEnd else j+1
              #Add in bold
              if(boldEnd):
                wrapped_lines[i] = wrapped_lines[i][:j] + '\u001b[0m' + wrapped_lines[i][j:]
              else:
                wrapped_lines[i] = wrapped_lines[i][:j] + '\u001b[1m' + wrapped_lines[i][j:]
              boldEnd = not boldEnd
              break
            else:
              wrapped_lines[i] = wrapped_lines[i][:j] + '\u0332' + wrapped_lines[i][j:]
          #Increase pos
          if(wrapped_lines[i][j] != '\n'): #Disregard added newlines
            pos += 1
    """
    #Get rid of any white space after newline
    for i in range(len(wrapped_lines)):
      wrapped_lines[i] = wrapped_lines[i].replace('\n ', '\n')

    #Combine list
    if(len(text) > 0 and text[-1] == '\n'):
      return '\n'.join(wrapped_lines) + '\n'
    return '\n'.join(wrapped_lines)

def print(value = "",
    sep: str | None = " ",
    end: str | None = "\n") -> None:
  return builtins.print(wrap_text_to_terminal(str(value)),sep=sep,end=end)

def input(prompt: object = ""):
  return builtins.input(wrap_text_to_terminal(str(prompt)))


if __name__ == "__main__":
  text = f"hello {underline('hel')+bold(underline('l'))+underline('o')} world {bold('world')}"
  print(text)

  #input("Hello:\n")
  #builtins.input("Hello:\n")
  #input("hi\n\n")
  #uiltins.input("hi\n\n")
  #input('eep')
  #builtins.input('eep')

  print(f"WOAHHHHH {bold('BOLDING')}")
  print(f"HOLLOY COW {underline('WE UNDERLINE')}")
  print("Omg this is such a long text woah i dont even know what to type this is so very long i hope this text wrapping stuff will work properly man let's just hope it works good okay yeah so like good luck i guess i dont know how well this will work.")
  input()
  print("Omg AGAIN this is such a long AGAIN text woah i dont even AGAIN know what to type this AGAIN is so very long i hope AGAIN this text wrapping stuff will work AGAIN properly man let's just hope it works good okay AGAIN yeah so like good luck i guess i dont know how well this AGAIN will work AGAIN.")
  print(123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890)