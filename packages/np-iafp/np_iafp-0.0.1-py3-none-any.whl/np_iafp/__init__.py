def primo(n):
	for i in range(2, n+1):
		es_primo = True
		for j in range(2, i):
			if(i%j == 0):
				es_primo = False
		if(es_primo):
			print(f"{i} es primo")