def args_demo(*args):
  print(type(args))
  print(args[3])


def kwargs_demo(**kwargs):
  print(type(kwargs))
  print(kwargs['name'])
kwargs_demo(name='John', age=30, city='New York')
args_demo(1, 2, 3, 4, 5)