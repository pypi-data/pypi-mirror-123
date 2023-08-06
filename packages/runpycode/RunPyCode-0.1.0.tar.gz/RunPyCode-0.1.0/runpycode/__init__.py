__version__ = '0.1.0'

def run(code):
  file = open("code.py", "w+")
  file.write(code)
  file.close()
  exec(open("code.py").read())
