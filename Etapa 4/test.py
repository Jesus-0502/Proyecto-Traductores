
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


program = (lambda x1: (lambda x1: ((apply(lambda x3: lambda x2: lambda x1: cons(x3)(cons(x2)(cons(3)(nil)))))(x1) if (apply(lambda x3: lambda x2: lambda x1: (x1>x2 and x1>0)))(x1) else ((apply(lambda x3: lambda x2: lambda x1: cons(x3)(cons(2)(cons(x1)(nil)))))(x1) if (apply(lambda x3: lambda x2: lambda x1: (x1 < x2)))(x1) else x1)))((apply(lambda x3: lambda x2: lambda x1: cons(x3)(cons(24)(cons(x1)(nil)))))((apply(lambda x3: lambda x2: lambda x1: cons(x3)(cons(x2)(cons(12)(nil)))))(x1))))

result = program(cons(0)(cons(0)(cons(0)(nil))))
print(apply(lambda c: lambda b: lambda a: {'a': a, 'b': b, 'c': c})(result))
