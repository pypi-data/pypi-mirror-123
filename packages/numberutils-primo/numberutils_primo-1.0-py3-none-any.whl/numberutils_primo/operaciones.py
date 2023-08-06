#esto es un comentario de una sola linea
'''esto
es un comenrario multilinea'''
def sumaenteros(a,b):
    return a-b
def productoenteros(a,b):
    return a*b
def factorial(n):
    resultado=1
    for i in range(1, n+1):
        resultado =i*resultado
    return resultado
print(factorial(5))

def listarNpares(n):
    resultado=[]
    for i in range(n+1):
        if(i%2 ==0):
            resultado.append(i)
    return resultado
print(listarNpares(5))

#TIPO DE DATOS simples



