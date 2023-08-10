import sys
import termios

def set_echo(x):
  fd = sys.stdin.fileno()
  attr = termios.tcgetattr(fd)
  if x:
    attr[3] |= termios.ECHO
  else:
    attr[3] &= ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, attr)

def write(s):
  print(s, end='')


def count_parens(s):
  n = 0
  for c in s:
    if c == '(':
      n += 1
    if c == ')':
      n -= 1
  return n

def nr_list_read(expr):
  expr = expr.strip()
  if expr[0] == ')':
    return [], expr[1:]
  first, s1 = nr_read(expr) 
  rest, s2 = nr_list_read(s1)
  return [first, *rest], s2

def nr_parse_atom(val):
  try:
    return int(val)
  except:
    try:
      return float(val)
    except:
      return val

def nr_read(expr):
  expr = expr.strip()
  if expr[0] == '(':
    return nr_list_read(expr[1:])
  if expr[0] == '#':
    lst, s = nr_list_read(expr[2:])
    return dict(lst), s
  val = expr.split()[0].split(')')[0]
  s = expr[len(val):]
  return nr_parse_atom(val), s
nr_read('(2 \n 1)')

nr_read('#((2 1))')


def car(expr):
  try:
    return expr[0]
  except:
    return []
assert(car([1, 2]) == 1)
assert(car(1) == [])

def cdr(expr):
  try:
    return expr[1:]
  except:
    return []
assert(cdr([1, 2, 3]) == [2, 3])

def cons(a, b):
  return [a, *b]

def assoc(arr, key):
  if arr == []:
    return []
  p = car(arr)
  if car(p) == key:
    return p
  return assoc(cdr(arr), key)
assoc([['a', 1], ['b', 2], ['c', 3]], 'b')



def nr_eval(env, expr):
  if isinstance(expr, str):
    return env[expr]
  if isinstance(expr, list):
    exop, payl = nr_eval(env, expr[0])
    return exop(env, payl, expr[1:])
  return expr

def nr_evlis(env, lst):
  return list(map(lambda expr: nr_eval(env, expr), lst))

#let's do a normal lisp first


def nr_add(env, payl, args):
  return sum(nr_evlis(env, args))

def nr_inop(env, payl, args):
  new_env = {**env, **dict(zip(payl['argsyms'], args))}
  return nr_eval(new_env, payl['code'])




env = {
  'a': 1,
  'b': 2,
  'c': 3,
  '+': [nr_add, {}],
  '*2': [
     nr_inop, {
       'code': ['+', 'x', 'x'],
       'argsyms': ['x']
     }
  ],
}
#nr_eval(env, 'a')
#nr_eval(env, '+')
nr_eval(env, ['+', 1, 2])
nr_eval(env, ['*2', 3])


def repl():
  try:
    set_echo(False)
    while True:
      buf = ''
      parens = count_parens(buf)
      while True:
        s = input() 
        parens += count_parens(s)
        buf += s
        if parens == 0:
          break
        buf += '\n  '
      expr, _ = nr_read(buf)
      ans = nr_eval(env, expr)
      write(f'\n\n> {buf}\n{ans}')
  except EOFError as e:
    set_echo(True)
    print(e)
repl()
  

