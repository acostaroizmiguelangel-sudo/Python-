class ColaArreglo:
    def __init__(self, tamano_max):
        self.max_size = tamano_max
        self.queue = [None] * tamano_max
        self.front = -1
        self.rear = -1

    def isFull(self):
        return (self.front == 0 and self.rear == self.max_size - 1) or (self.front == self.rear + 1)

    def isEmpty(self):
        return self.front == -1

    def enqueue(self, data):
        if self.isFull():
            print("Error: Cola desbordada (Overflow)")
            return
        
        if self.front == -1:
            self.front = 0
            
        self.rear = (self.rear + 1) % self.max_size
        self.queue[self.rear] = data

    def dequeue(self):
        if self.isEmpty():
            print("Error: Cola subdesbordada (Underflow)")
            return None
        
        data = self.queue[self.front]
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.max_size
        return data

    def peek(self):
        if self.isEmpty():
            print("Cola vacía")
            return None
        return self.queue[self.front]

if __name__ == "__main__":
    cola = ColaArreglo(5)
    cola.enqueue(10)
    cola.enqueue(20)
    cola.enqueue(30)
    
    print(f"Elemento frontal: {cola.peek()}")
    print(f"Elimina elemento: {cola.dequeue()}")
    print(f"Nuevo elemento frontal: {cola.peek()}")
    
    cola.enqueue(40)
    cola.enqueue(50)
    cola.enqueue(60) 
    print(f"Elimina elemento: {cola.dequeue()}")