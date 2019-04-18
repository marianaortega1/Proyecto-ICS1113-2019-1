from gurobipy import *

# Definicion de data: Definir conjuntos P,M y T
products = ["Prod1", "Prod2", "Prod3", "Prod4", "Prod5", "Prod6", "Prod7"]
machines = ["grinder", "vertDrill", "horiDrill", "borer", "planer"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]


# Valores para el parámetro k_p (Contribución de ganancias por producto), cantidad de máquinas
profit_contribution = {"Prod1": 10, "Prod2": 6, "Prod3" : 8, "Prod4": 4, "Prod5": 11, "Prod6": 9, "Prod7": 3}
qMachine = {"grinder": 4, "vertDrill": 2, "horiDrill": 3, "borer": 1, "planer": 1}

# Tiempo de producción requerido por producto por máquina f_p,m
time_table = {
    "grinder" : {"Prod1": 0.5, "Prod2": 0.7, "Prod5": 0.3, "Prod6": 0.2, "Prod7": 0.5},
    "vertDrill": {"Prod1": 0.1, "Prod2": 0.2, "Prod4": 0.3, "Prod6": 0.6},
    "horiDrill": {"Prod1": 0.2, "Prod3": 0.8, "Prod7": 0.6},
    "borer": {"Prod1": 0.05, "Prod2": 0.03, "Prod4": 0.07, "Prod5": 0.1, "Prod7": 0.08},
    "planer": {"Prod3": 0.01, "Prod5": 0.05, "Prod7": 0.05}
}

# Numero de maquinas no funcionales por mantenimiento por mes por tipo de maquina
down= {("Jan", "grinder"): 1, ("Feb", "horiDrill"): 2, ("Mar", "borer"): 1, ("Apr", "vertDrill"): 1,
       ("May", "grinder"): 1, ("May", "vertDrill"): 1, ("Jun", "horiDrill"): 1}


# Limite de ventas por mes por producto
upper ={
    "Jan": {"Prod1": 500, "Prod2": 1000, "Prod3": 300, "Prod4": 300, "Prod5": 800, "Prod6": 200, "Prod7": 100},
    "Feb": {"Prod1": 600, "Prod2": 500, "Prod3": 200, "Prod4": 0, "Prod5": 400, "Prod6": 300, "Prod7": 150},
    "Mar": {"Prod1": 300, "Prod2": 600, "Prod3": 0, "Prod4": 0, "Prod5": 500, "Prod6": 400, "Prod7": 100},
    "Apr": {"Prod1": 200, "Prod2": 300, "Prod3": 400, "Prod4": 500, "Prod5": 200, "Prod6": 0, "Prod7": 100},
    "May": {"Prod1": 0, "Prod2": 100, "Prod3": 500, "Prod4": 100, "Prod5": 1000, "Prod6": 300, "Prod7": 0},
    "Jun": {"Prod1": 500, "Prod2": 500, "Prod3": 100, "Prod4": 300, "Prod5": 1100, "Prod6": 500, "Prod7": 60}
}

# parametros constantes
r = 0.5
z = 100
w = 50
g = 2*8*24

# Generación del modelo
model = Model("Factory Planning Equipo Rocket")

manu = model.addVars(months, products, vtype=GRB.INTEGER, name="manu")
held = model.addVars(months, products, vtype=GRB.INTEGER, name="held", ub=z)
sell = model.addVars(months, products, vtype=GRB.INTEGER, name="sell",
                     ub=[upper[month][product] for month in months for product in products])


# Llama a update para agregar las variables al modelo
model.update()

# Restricciones de inventario
# Primer mes
model.addConstrs((manu[month, product] == sell[month, product] + held[month, product]
                  for month_index, month in enumerate(months) for product in products if month_index == 0),
                 name="balance")
# Resto de meses
model.addConstrs((held[months[month_index-1], product] + manu[month, product] ==
                  sell[month, product] + held[month, product]
                  for month_index, month in enumerate(months) for product in products if month_index != 0),
                 name="balance")


# Restriccion que fuerza que al final del último mes haya una cantidad específica almacenada de cada producto

model.addConstrs((held[months[-1], product] == w for product in products), name="endstock")

# Restricción de almacenaje según capacidad de la tienda
model.addConstrs((held[month, product] <= z for month in months for product in products),
                 name="storeCapacity")

# Restriccion de no sobrepasar maximo de horas disponibles
model.addConstrs((quicksum(time_table[machine][product] * manu[month, product] for product in time_table[machine]) <=
                  g * (qMachine[machine] - down[month, machine])
                  for month in months
                  for machine in machines
                  if (month, machine) in down), name="capacity")

model.addConstrs((quicksum(time_table[machine][product] * manu[month, product] for product in time_table[machine]) <=
                  g * qMachine[machine]
                  for month in months
                  for machine in machines
                  if (month, machine) not in down), name="capacity")

# Restricción de la cantidad máxima que se puede vender de cada producto en cada mes
model.addConstrs(sell[month, product] <= upper[month][product] for month in months for product in products)

# Funcion objetivo
obj = quicksum(
    profit_contribution[product] * sell[month, product] - r * held[month, product]
    for month in months
    for product in products)

model.setObjective(obj, GRB.MAXIMIZE)


model.optimize()

# Mostrar los valores de las soluciones
model.printAttr("X")


