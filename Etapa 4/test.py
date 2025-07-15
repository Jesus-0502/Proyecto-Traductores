
Z = lambda g:(lambda x:g(lambda v:x(x)(v)))(lambda x:g(lambda v:x(x)(v)))
true = lambda x:lambda y:x
false = lambda x:lambda y:y
nil = lambda x:true
cons = lambda x:lambda y:lambda f: f(x)(y)
head = lambda p: p(true)
tail = lambda p:p(false)
apply = Z(lambda g:lambda f:lambda x:f if x==nil else (g(f(head(x)))(tail(x))))


program = (lambda initial: (apply(lambda x3: lambda x2: lambda x1: cons(x2)(cons(x3)(cons(12)(nil)))))((apply(lambda x3: lambda x2: lambda x1: cons(x2)(cons(x3)(cons(((((a + b) + (((c - 0) * (a - 0)) * b)) - a) - b))(nil)))))(initial)))

result = program(cons(0)(cons(0)(cons(0)(nil))))
print(apply(lambda c: lambda b: lambda a: {'a': a, 'b': b, 'c': c})(result))
