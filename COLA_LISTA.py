class Nodo:
    def __init__(self, data):
        self.data = data
        self.next = None

class ColaLista:
    def __init__(self):
        self.front = None
        self.rear = None

    def isEmpty(self):
        return self.front is None

    def enqueue(self, data):
        nuevo_nodo = Nodo(data)
        if self.rear is None:
            self.front = nuevo_nodo
            self.rear = nuevo_nodo
            return
        self.rear.next = nuevo_nodo
        self.rear = nuevo_nodo

    def dequeue(self):
        if self.isEmpty():
            print("Error: Cola subdesbordada (Underflow)")
            return None
        
        data = self.front.data
        self.front = self.front.next
        
        if self.front is None:
            self.rear = None
        return data

    def peek(self):
        if self.isEmpty():
            print("Cola vacía")
            return None
        return self.front.data

if __name__ == "__main__":
    cola = ColaLista()
    cola.enqueue(10)
    cola.enqueue(20)
    cola.enqueue(30)
    
    print(f"Elemento frontal: {cola.peek()}")
    print(f"Elimina elemento: {cola.dequeue()}")
    print(f"Nuevo elemento frontal: {cola.peek()}")
    
    cola.enqueue(40)
    print(f"Elimina elemento: {cola.dequeue()}")
    print(f"Elimina elemento: {cola.dequeue()}")
    print(f"Elimina elemento: {cola.dequeue()}")
    print(f"Elimina elemento: {cola.dequeue()}")