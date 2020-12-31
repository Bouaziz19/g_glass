a=0
excod=compile('a = 3; a = a + 10; print(a)', '<string>', 'exec')
exec(excod)
print(a)