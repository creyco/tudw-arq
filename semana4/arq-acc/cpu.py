import sys
from assembly import ASSEMBLY

'''
- Crear una clase CLOCK, 
- Atributos de clase - No
- con atributo: ciclos
- su constructor y metodos:
    CountCycles - suma 1 ciclo
    WaitCycles  - suma 4 ciclos
'''

class CLOCK:
    def __init__(self):
        self.cycles = 0

    def CountCycles(self):
        self.cycles += 1

    def WaitCycles4(self):
        self.cycles += 4

'''
Crear una clase CPU
- Variables de clase - No
    Atributos: 
'''

class CPU:
    def __init__(self):
        
        #Registers PC, ACC, IR, MDR, MAR
        self.PC = 0     # contador de programa
        self.ACC = 0    # Acumulador -> resultados -> intermedio
        self.IR = 0     # Registro de Instrucciones
        self.MDR = 0    # Datos de memoria
        self.MAR = 0    # direcciones de memoria

        #RAM or self.memory, 6 bit address 
        #bus --> 2^6 = 64 bytes of RAM
        self.memory = [0]*64

        #Flags
        self.HLT = False        # Atributo detener
        self.clock = CLOCK()    # instancia Reloj

    def loadProgram(self, code):
        self.memory = list(code)  

    def fetch(self):
        #fetch instruction  -> busca instruccion
        print(f"------------------memory[{self.PC}]-------------------------")
        self.MAR = self.PC
        self.clock.CountCycles()
        self.MDR = self.memory[self.MAR]
        self.PC += 1            # suma una instruccion
        self.clock.CountCycles()       
         #wait memory
        self.clock.WaitCycles4()
        self.IR = self.MDR
        self.clock.CountCycles() 
        print (f"fetching memory[{self.PC-1}] => IR({self.IR}) ← PC({self.PC-1})")

    def execute(self):
        #decode instruction from opcode by masking higher 6 bits
        opcode = (self.IR >> 6)
        address = (self.IR & 0x3F)
        #print(f"IR (opcode|address)= {opcode}|{address}")
        #input("...")
        
        #execute
        if(opcode == 0x0):
            #LDA
            self.MAR =  address
            self.clock.CountCycles()
            self.MDR =  self.memory[self.MAR]
            self.clock.CountCycles()       
            #wait memory
            self.clock.WaitCycles4()
            self.ACC =  self.MDR
            self.clock.CountCycles()       
            print(f"executing LDA {self.MAR}    => ACC({self.ACC}) ← memory[{self.MAR}]")
           
        elif(opcode == 0x1):   
            #STA
            self.MAR = address
            self.clock.CountCycles()       
            self.MDR = self.ACC 
            self.clock.CountCycles()
            self.memory[self.MAR] = self.MDR 
            self.clock.CountCycles()       
            #wait memory
            self.clock.WaitCycles4()
            print(f"executing STA {self.MAR}    => memory[{self.MAR}] ← ACC({self.ACC})")
        elif(opcode == 0x2):   
            #ADD
            self.MAR = address
            self.clock.CountCycles() 
            self.MAR = self.memory[self.MAR]
            self.clock.CountCycles()       
            #wait memory
            self.clock.WaitCycles4()
            print(f"executing ADD {self.MAR}    => ACC({self.ACC + self.MDR}) ← ACC({self.ACC}) + MDR({self.MDR})")
            self.ACC = self.ACC + self.MDR 
            self.clock.CountCycles()            
        elif(opcode == 0x3):   
            #HLT
            self.HLT = True
            self.clock.CountCycles()
            print("executing HLT      => stop CPU")
        else:
            print(f"Illegal opcode {hex(opcode)}")


def main(filename):
    cpu = CPU()
    asm = ASSEMBLY()
    
    asm.assembler(filename)
    cpu.loadProgram(asm.code)

    while not cpu.HLT: 
        
        try:
            #stage fetch
            cpu.fetch()
           
            #stage execution
            cpu.execute()
            
        except Exception as e:
            print("HALTING System...")
            break;
    print(" ---------------------------------------------------")
    print(f"Program-Cycles: {cpu.clock.cycles}")
    print(f"     RI:    {cpu.PC}" )
    print(f"     CPI: {cpu.clock.cycles / cpu.PC}" )   
    print(f"Time CPU: {cpu.clock.cycles * cpu.PC * cpu.clock.cycles / cpu.PC }  ")
    print(" -------------------------------------------")

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except:
        print("-------------------------------------------")
        print("|Usage: python cpu.py  <asm filename>      |")
        print("|Example win: python cpu.py code.asm       |")
        print("|Example linux: python3 cpu.py code.asm    |")
        print(" ------------------------------------------\n")
        exit()
    main(filename)
