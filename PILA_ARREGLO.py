class PilaArreglo:
    def __init__(self, tamano_max):
        self.stack = [None] * tamano_max
        self.max_size = tamano_max
        self.top = -1

    def isEmpty(self):
        return self.top == -1

    def isFull(self):
        return self.top == self.max_size - 1

    def push(self, data):
        if self.isFull():
            print("Error: Stack Overflow")
            return
        self.top += 1
        self.stack[self.top] = data

    def pop(self):
        if self.isEmpty():
            print("Error: Stack Underflow")
            return -1
        data = self.stack[self.top]
        self.top -= 1
        return data

    def peek(self):
        if self.isEmpty():
            print("Pila vacía")
            return -1
        return self.stack[self.top]

if __name__ == "__main__":
    pila = PilaArreglo(100)
    pila.push(10)
    pila.push(20)
    pila.push(30)
    
    print(f"Elemento superior: {pila.peek()}")
    print(f"Extrae elemento: {pila.pop()}")
    print(f"Nuevo elemento superior: {pila.peek()}")