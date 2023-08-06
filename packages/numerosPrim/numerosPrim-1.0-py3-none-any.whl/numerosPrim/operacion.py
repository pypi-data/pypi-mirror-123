def numero_primo(n):
	for i in range(2, n):
		numeroPrimo = True
		for x in range(2, i):
			if(i% x == 0):
				numeroPrimo = False
		if(numeroPrimo):
			print('NUMERO PRIMO'.center(30,'*'))
			print(f"El número {i} es primo")

