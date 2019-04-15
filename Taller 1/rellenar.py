from gurobipy import Model, GRB

# Definicion de data: Definir conjuntos P,M y T
products = ["Prod1", "Prod2", "Prod3", "Prod4", "Prod5", "Prod6", "Prod7"]
machines = ["grinder", "vertDrill", "horiDrill", "borer", "planer"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

# Definir valores para el parámetro k_p (Contribución de ganancias por producto) y cantidad de máquinas
profit_contribution = {"Prod1": 30, "Prod2": 6, "Prod3" : 8, "Prod4": 4, "Prod5": 11, "Prod6": 9, "Prod7": 3}
qMachine = {"grinder": 4, "vertDrill": 2, "horiDrill": 3, "borer": 1, "planer": 1}

# Definir tiempo de producción requerido por producto por máquina f_p,m
time_table = {
    "grinder" : {"Prod1": 0.5, "Prod2": 0.7, "Prod5": 0.3, "Prod6": 0.2, "Prod7": 0.5},
    "vertDrill": {"Prod1": 0.1, "Prod2": 0.2, "Prod4": 0.3, "Prod6": 0.6},
    "horiDrill": {"Prod1": 0.2, "Prod3": 0.8, "Prod7": 0.6},
    "borer": {"Prod1": 0.05, "Prod2": 0.03, "Prod4": 0.07, "Prod5": 0.1, "Prod7": 0.08},
    "planer": {"Prod3": 0.01, "Prod5": 0.05, "Prod7": 0.05}
}

# Definir numero de maquinas no funcionales por mantenimiento por mes por tipo de maquina
down = {("Jan", "grinder"): 1, ("Feb", "horiDrill"): 2, ("Mar", "borer"): 1, ("Apr", "vertDrill"): 1,
       ("May", "grinder"): 1, ("May", "vertDrill"): 1, ("Jun", "horiDrill"): 1}

# Ahora tú define un diccionario con el limite de ventas por mes por producto. Puedes guarte con el time_table.
upper = {}

# parametros constantes
storeCost = 0.5
storeCapacity = 100
endStock = 50
hoursPerMonth = 2*8*24

# Creamos un modelo vacío
model = Model("Factory Planning Equipo Rocket")

# Crea y rellenar diccionarios de variables manufactura b_t,p , almacenada s_t,p , vendida u_t,p
# Por ejemplo para la variable de manfucatura hacemos lo siguiente
manu = {} #Cantidad manufacturada

for month in months:
    for product in products:
        manu[month, product] = model.addVar(vtype=GRB.INTEGER, name="manu_{}_{}".format(month, product))

# Llama a update para agregar las variables al modelo

# Crea restricciones de inventario

# Crea la restriccion que fuerza que al final de los meses la cantidad almacenada sea la cantidad especifica
# de cada producto

# Restricción de almacenaje según capacidad de la tienda

# Restriccion de no sobrepasar maximo de horas disponibles

# Funcion objetivo

# Optimiza tu problema

# Muestra los valores de las soluciones


