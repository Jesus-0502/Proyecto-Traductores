
Z = lambda g:(lambda x:g(lambda v:x(x)(v)))(lambda x:g(lambda v:x(x)(v)))
true = lambda x:lambda y:x
false = lambda x:lambda y:y
nil = lambda x:true
cons = lambda x:lambda y:lambda f: f(x)(y)
head = lambda p: p(true)
tail = lambda p:p(false)
apply = Z(lambda g:lambda f:lambda x:f if x==nil else (g(f(head(x)))(tail(x))))
lift_do=lambda exp:lambda f:lambda g: lambda x: g(f(x)) if (exp(x)) else x
do=lambda exp:lambda f:Z(lift_do(exp)(f))


program = (lambda x1: (lambda x1: ((apply(lambda x2: lambda x1: cons(True)(cons(x1)(nil))))(x1) if (apply(lambda x2: lambda x1: x1 or True))(x1) else x1))(x1))

result = program(cons(False)(cons(False)(nil)))
print(apply(lambda b: lambda a: {'a': a, 'b': b})(result))
