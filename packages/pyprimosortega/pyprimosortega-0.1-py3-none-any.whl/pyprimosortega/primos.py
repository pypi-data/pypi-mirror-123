num = float(input("introduce un número positivo: "))

if (num > 0):
    print("Bien elegido")

else: print("El número elegido no es positivo")

parteentera = int(num)

def listadeprimos(n):

    primos = []

    for i in range(1,n+1):

        if (i <= 3):
            primos.append(i)
        else:
            k = 2
            for j in range (2,i):
                if (i % j != 0):
                   k += 1 
            if (k==i):
                primos.append(i)
    
    return primos

lista = listadeprimos(parteentera)
print(lista)
print("Hay",len(lista)," números primos entre 1 y", num)