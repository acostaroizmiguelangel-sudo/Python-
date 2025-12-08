class Nodo:
    def __init__(self, data):
        self.data = data
        self.next = None

class PilaLista:
    def __init__(self):
        self.top = None

    def isEmpty(self):
        return self.top is None

    def push(self, data):
        nuevo_nodo = Nodo(data)
        nuevo_nodo.next = self.top
        self.top = nuevo_nodo

    def pop(self):
        if self.isEmpty():
            print("Error: Stack Underflow")
            return None
        data = self.top.data
        self.top = self.top.next
        return data

    def peek(self):
        if self.isEmpty():
            print("Pila vacía")
            return None
        return self.top.data

if __name__ == "__main__":
    pila = PilaLista()
    pila.push(10)
    pila.push(20)
    pila.push(30)
    
    print(f"Elemento superior: {pila.peek()}")
    print(f"Extrae elemento: {pila.pop()}")
    print(f"Nuevo elemento superior: {pila.peek()}")