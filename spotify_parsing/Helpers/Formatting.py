import shutil
import textwrap
import builtins

def bold(s:str)->str:
  """Formats to bold given string when printed in console"""
  ###Look into blessed to make UI a bit more pretty (may need big overhaul...)
  return f'\u001b[1m{s}\u001b[0m'

def underline(s:str)->str:
  """Formats to underline given string when printed in console. Note: only letters can be underlined"""
  return '\u0332'.join(s + ' ')[:-1]


def wrap_text_to_terminal(text: str) -> str:
    """Wraps text to the current terminal width using textwrap."""
    try:
        terminal_size = shutil.get_terminal_size()  #Get terminal dimensions
        width = terminal_size.columns #Extract the width
    except (AttributeError, OSError):
        #Fallback if broken (105 is default width of terminal for my laptop)
        width = 105
    
    splittedText = text.splitlines()
    wrapped_lines = [textwrap.fill(line,width=width, drop_whitespace=False, replace_whitespace=False) for line in splittedText]
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
  input("Hello:\n")
  builtins.input("Hello:\n")
  input("hi\n\n")
  builtins.input("hi\n\n")
  input('eep')
  builtins.input('eep')

  print(f"WOAHHHHH {bold('BOLDING')}")
  print(f"HOLLOY COW {underline('WE UNDERLINE')}")
  print("Omg this is such a long text woah i dont even know what to type this is so very long i hope this text wrapping stuff will work properly man let's just hope it works good okay yeah so like good luck i guess i dont know how well this will work.")
  input()
  print("Omg AGAIN this is such a long AGAIN text woah i dont even AGAIN know what to type this AGAIN is so very long i hope AGAIN this text wrapping stuff will work AGAIN properly man let's just hope it works good okay AGAIN yeah so like good luck i guess i dont know how well this AGAIN will work AGAIN.")
  print(123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890)