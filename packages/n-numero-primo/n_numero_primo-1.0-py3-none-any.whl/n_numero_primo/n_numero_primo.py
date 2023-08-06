def primo(numero):
    contador = 0
    for i in range(1,numero+1): # codigo c++   for(int i=1;i<=numero;i++)
        if(numero%i==0):
            contador=contador+1
    if(contador<=2):
        return "Es un numero Primo"
    else:
        return "No es un numero Primo"

numero=int(input("Ingresar numero:"))
print(primo(numero))
