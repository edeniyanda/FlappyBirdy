import timeit

setup = '''
class Test:
    def __init__(self):
        self.velocity = 0
t = Test()
'''

code_conditional = '''
if t.velocity < 8:
    t.velocity += 0.5
else:
    t.velocity = 8
'''

code_min_function = '''
t.velocity = min(t.velocity + 0.5, 8)
'''

# Benchmark conditional expression
time_conditional = timeit.timeit(code_conditional, setup=setup, number=1000000)

# Benchmark min function
time_min_function = timeit.timeit(code_min_function, setup=setup, number=1000000)

print(f"Conditional: {time_conditional} seconds")
print(f"min function: {time_min_function} seconds")
