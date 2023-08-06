__version__ = '0.1.1'

def run(code):
  file = open("code.py", "w+")
  file.write(code)
  file.close()
  exec(open("code.py").read())

def write(text):
  print(text)