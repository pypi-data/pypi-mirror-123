def primo(n): #A la función le pasamos un número, este número va a ser el tope para comprobar si los números anteriores a este son primos
	for i in range(2, n): #Se crea un bucle que empieza en 2 y termina en el número pasado a la función menos 1 (n-1), los valores de cada iteración se guardan en la variable 'i'
		es_primo = True #Inicializamos la variable 'es_primo' con el valor True (Verdadero)
		for j in range(2, i): #Se crea un bucle que va a empezar en 2 y va a terminar en el valor de 'i' en este momento menos 1 (i-1), los valores de cada iteración se guardan en la variable 'j'
			if(i%j == 0): # Si el resto de la división de el valor de 'i' entre el valor de 'j' es igual a 0 quiere decir que el número contenido en 'i' no es primo y la variable 'es_primo' va a tener el valor de 'False'
				es_primo = False
		if(es_primo): #Si es_primo es 'True' (Verdadero) se va a sacar por pantalla los números primos
			print(f"{i} es primo")