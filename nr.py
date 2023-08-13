import os
import sys
import termios
import ast

def stty(x):
  os.system(f'stty {x}')


def count_parens(s):
  n = 0
  for c in s:
    if c == '(':
      n += 1
    if c == ')':
      n -= 1
  return n
assert(count_parens('') == 0)
assert(count_parens(')') == -1)
assert(count_parens('(') == 1)
assert(count_parens('(())()((') == 2)


def nr_parse_atom(val):
  if val in ['NaN', 'inf', '-inf']: 
    return float(val)
  try:
    return ast.literal_eval(val)
  except:
    return val
assert(type(nr_parse_atom('')) == str)
assert(type(nr_parse_atom('dffd')) == str)
assert(type(nr_parse_atom('1')) == int)
assert(type(nr_parse_atom('-1')) == int)
assert(type(nr_parse_atom('0x19')) == int)
assert(type(nr_parse_atom('-0x19')) == int)
assert(type(nr_parse_atom('0.0')) == float)
assert(type(nr_parse_atom('inf')) == float)
assert(type(nr_parse_atom('2.9e9')) == float)
assert(nr_parse_atom('19') == 19)
#type(nr_parse_atom('-0b19')) #TODO - raise exception for invalid digits


def nr_list_read(expr):
  expr = expr.strip()
  if expr[0] == ')':
    return [], expr[1:]
  first, s1 = nr_read(expr) 
  rest, s2 = nr_list_read(s1)
  return [first, *rest], s2

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


def nr_eval(env, expr):
  if isinstance(expr, str):
    return env[expr]
  if isinstance(expr, list):
    exop, payl = nr_eval(env, expr[0])
    return exop(env, payl, expr[1:])
  return expr

def nr_list(env, lst):
  return list(map(lambda expr: nr_eval(env, expr), lst))



def op_inop(env, payl, args):
  new_env = {**env, **dict(zip(payl['argsyms'], nr_list(env, args)))}
  return nr_eval(new_env, payl['code'])

def op_dict(env, payl, args):
  return dict(nr_list(env, args))

#TODO implicit progn
def op_fn(env, payl, args):
  return [op_inop, {'code': args[1], 'argsyms': args[0]}]

def op_quote(env, payl, args):
  return args[0]

def op_list(env, payl, args):
  return nr_list(env, args)

def op_car(env, payl, args):
  return nr_eval(env, args[0])[0]

def op_cdr(env, payl, args):
  return nr_eval(env, args[0])[1:]

def op_cons(env, payl, args):
  return [nr_eval(env, args[0]), *nr_eval(env, args[1])]

def op_if(env, payl, args):
  if nr_eval(env, args[0]) != []:
    return nr_eval(env, args[1])
  else:
    return nr_eval(env, args[2])

def op_def(env, payl, args):
  env[args[0]] = nr_eval(env, args[1])
  return args[0]

def op_add(env, payl, args):
  return sum(nr_list(env, args))

def op_sub(env, payl, args):
  return nr_eval(env, args[0]) - nr_eval(env, args[1])

env = {
  '~': [],
  "'": [op_quote, {}],
  '+': [op_add, {}],
  '-': [op_sub, {}],
  '<': [op_car, {}],   
  '>': [op_cdr, {}],   
  'if': [op_if, {}],
  'cons': [op_cons, {}],
  'l': [op_list, {}],
  'fn': [op_fn, {}],
  'def': [op_def, {}],
  '*2': [
     op_inop, 
     {
       'code': ['+', 'x', 'x'],
       'argsyms': ['x']
     }
  ],
}
#nr_eval(env, 'a')
#nr_eval(env, '+')
#nr_eval(env, ['+', 1, 2])

def write(s):
  print(s, end='')

def repl():
  try:
    stty('-echo')
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
      if buf.strip() != '':
        expr, _ = nr_read(buf)
        ans = nr_eval(env, expr)
        write(f'\n\n> {buf}\n{ans}')
  except EOFError:
    pass
  finally:
    stty('echo')
repl()  


