import random
elements = 100 #общее количество элементов
numbers = [random.randint(3000,9000) for _ in range(elements)]
# numbers = [5500,3000,2500,2000,6548,9800,9000,2300,5500,5600,5200,6100,7200,2100,2700,3500,4300,4200,4000,3900]
n = 5 #по сколько элементов в группе
m = len(numbers)//n #количество групп
print(f"Числа: {numbers}")
print(f"Разбить {len(numbers)} чисел на группы по {n} числа")
numbers = sorted(numbers)
for i in range(m):
	group = []
	while len(group) != (elements//m-1):
		group.append(numbers.pop(1))
		group.append(numbers.pop(-1))
	group.append(numbers.pop(len(numbers)//2-1))
	print(f"{group} = {sum(group)}")