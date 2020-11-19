from environment import Environment
from robot import action
from tqdm import tqdm
from colorama import Fore, Back, Style 


class Main:
    def __init__(self, settings):
        self.settings=settings
    
    def start(self):
        print("COMENZANDO EXPERIMENTO...")
        for item in self.settings:
            e=Experiment(item[0], item[1], item[2], item[3], item[4])
            e.experiment(30)

class Experiment:
    def __init__(self, m, n, kids, obstacle_percentage, dirt_percentage):
        self.simulation=Simulation(m, n, kids, obstacle_percentage, dirt_percentage)
        self.success=0
        self.failure=0
        self.mean_dirt_percentage=0
        
    def experiment(self, n):
        self.__reset__()
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print(Fore.GREEN + "\nAMBIENTE:"+ Style.RESET_ALL +f"\n{self.simulation.m} filas y {self.simulation.n} columnas\n{self.simulation.kids} niños\n{self.simulation.obstacle_percentage}% de obstáculos\n{self.simulation.dirt_percentage}% de suciedad")
        print(Fore.RED)
        for i in tqdm(range(n)):
            result, mean_dirt=self.simulation.simulate(100*5, 5)
            if result=="FAILURE":
                self.failure+=1
            if result=="SUCCESS":
                self.success+=1
            self.mean_dirt_percentage=(mean_dirt*100)/(self.simulation.m*self.simulation.n)
            
        print(Style.RESET_ALL+self.__stats__(n))
        
    def __reset__(self):
        self.failure=0
        self.success=0
            
    def __stats__(self, n):
        return f'PORCIENTO DE EXITO: {(self.success*100)/n} \nPORCIENTO DE FALLO: {(self.failure*100)/n}\nPORCIENTO MEDIO DE CASILLAS SUCIAS: {self.mean_dirt_percentage}\n'

class Simulation:
    def __init__(self,m, n, kids, obstacle_percentage, dirt_percentage):
        self.m=m
        self.n=n
        self.obstacle_percentage=obstacle_percentage
        self.dirt_percentage=dirt_percentage
        self.kids=kids
        
    def simulate(self, n, t, verbose=False):
        self.environment=Environment(self.m, self.n, self.kids, self.obstacle_percentage, self.dirt_percentage)
        mean_dirt=0
        for count in range(n):
            if verbose:
                print(self.environment)
            mean_dirt+=self.environment.dirt
            if not count%t:
                self.environment.variate()
            action(self.environment)
            
            if self.environment.is_chaos():
                return "FAILURE", mean_dirt/count
            if self.environment.is_neat():
                return "SUCCESS", mean_dirt/count
        return "NONE", mean_dirt/n


  
m=Main([[3, 3, 1,  10, 10],
        [3, 3, 2,  10, 10],
        [3, 3, 3,  10, 10],
        [5, 5, 5,  10, 10],
        [5, 5, 5,  10, 20],
        [5, 5, 5,  10, 30],
        [10, 10, 7,  10, 10], 
        [10, 10, 7,  10, 20], 
        [10, 10, 7,  10, 30], 
        [10, 10, 10,  10, 10], 
        [10, 10, 20,  10, 10], 
        [10, 10, 30,  10, 10], 
])

m.start()

single=Simulation(5, 5, 5, 10, 10)
single.simulate(10, 2, True)
        