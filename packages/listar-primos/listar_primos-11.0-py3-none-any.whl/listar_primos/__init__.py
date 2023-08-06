def numberutilsprimo_total(a):
    def es_primo(num):
        for n in range(2, num):
            if num % n == 0:
                #print("No es primo", n, "es divisor")
                return False
        #print("Es primo")
        return True
    resultado=[]
    for i in range (2,a):
        if es_primo(i):
            resultado.append(i)
    return resultado

numberutilsprimo_total(1000)