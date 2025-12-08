class NodoDoble:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class ListaDoblementeCircular:
    def __init__(self):
        self.head = None

    def insertar_al_principio(self, data):
        nuevo_nodo = NodoDoble(data)
        if self.head is None:
            self.head = nuevo_nodo
            nuevo_nodo.next = self.head
            nuevo_nodo.prev = self.head
        else:
            tail = self.head.prev
            nuevo_nodo.next = self.head
            self.head.prev = nuevo_nodo
            self.head = nuevo_nodo
            self.head.prev = tail
            tail.next = self.head

    def insertar_al_final(self, data):
        nuevo_nodo = NodoDoble(data)
        if self.head is None:
            self.head = nuevo_nodo
            nuevo_nodo.next = self.head
            nuevo_nodo.prev = self.head
        else:
            tail = self.head.prev
            tail.next = nuevo_nodo
            nuevo_nodo.prev = tail
            nuevo_nodo.next = self.head
            self.head.prev = nuevo_nodo

    def imprimir_lista(self):
        if self.head is None:
            print("None")
            return
        
        nodo_actual = self.head
        while True:
            print(nodo_actual.data, end=" <-> ")
            nodo_actual = nodo_actual.next
            if nodo_actual == self.head:
                break
        print(f"(vuelve a {self.head.data})")

    def buscar(self, data_buscada):
        if self.head is None:
            return False
            
        nodo_actual = self.head
        while True:
            if nodo_actual.data == data_buscada:
                return True
            nodo_actual = nodo_actual.next
            if nodo_actual == self.head:
                break
        return False

    def eliminar(self, data_a_eliminar):
        if self.head is None:
            return

        nodo_actual = self.head
        while True:
            if nodo_actual.data == data_a_eliminar:
                break
            nodo_actual = nodo_actual.next
            if nodo_actual == self.head:
                return 

        if nodo_actual == self.head and self.head.next == self.head:
            self.head = None
            return

        if nodo_actual == self.head:
            self.head = nodo_actual.next

        nodo_actual.prev.next = nodo_actual.next
        nodo_actual.next.prev = nodo_actual.prev

if __name__ == "__main__":
    mi_lista = ListaDoblementeCircular()
    mi_lista.insertar_al_final(10)
    mi_lista.insertar_al_final(20)
    mi_lista.insertar_al_final(30)
    mi_lista.imprimir_lista()

    mi_lista.insertar_al_principio(5)
    mi_lista.imprimir_lista()

    print(f"¿Está el 20? {mi_lista.buscar(20)}")
    print(f"¿Está el 99? {mi_lista.buscar(99)}")

    mi_lista.eliminar(20)
    mi_lista.imprimir_lista()
    
    mi_lista.eliminar(5)
    mi_lista.imprimir_lista()
    
    mi_lista.eliminar(30)
    mi_lista.imprimir_lista()