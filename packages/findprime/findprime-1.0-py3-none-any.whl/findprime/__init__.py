def primo(n):
   for i in range(2,n):
        primo = True
        for j in range(2,i):
            if(i%j == 0):
                primo = False
        if(primo):
            print( f"{i} es primo")
primo(6)