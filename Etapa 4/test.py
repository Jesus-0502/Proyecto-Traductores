
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


program = (lambda x1: (apply(lambda x6: lambda x5: lambda x4: lambda x3: lambda x2: lambda x1: cons(x6)(cons(x5)(cons(3<=4)(cons(x3)(cons(x2)(cons(x1)(nil))))))))((apply(lambda x6: lambda x5: lambda x4: lambda x3: lambda x2: lambda x1: cons([3, 2, 1])(cons(x5)(cons(x4)(cons(x3)(cons(x2)(cons(x1)(nil))))))))(x1)))

result = program(cons([0, 0, 0])(cons(False)(cons(False)(cons(0)(cons(0)(cons(0)(nil)))))))
print(apply(lambda f: lambda e: lambda d: lambda c: lambda b: lambda a: {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f})(result))
