class Nodo:
    def __init__(self, data):
        self.data = data
        self.next = None

class ListaEnlazada:
    def __init__(self):
        self.head = None

    def insertar_al_principio(self, data):
        nuevo_nodo = Nodo(data)
        nuevo_nodo.next = self.head
        self.head = nuevo_nodo

    def insertar_al_final(self, data):
        nuevo_nodo = Nodo(data)
        if self.head is None:
            self.head = nuevo_nodo
            return

        ultimo_nodo = self.head
        while ultimo_nodo.next:
            ultimo_nodo = ultimo_nodo.next
        
        ultimo_nodo.next = nuevo_nodo

    def imprimir_lista(self):
        nodo_actual = self.head
        while nodo_actual:
            print(nodo_actual.data, end=" -> ")
            nodo_actual = nodo_actual.next
        print("None")

    def buscar(self, data_buscada):
        nodo_actual = self.head
        while nodo_actual:
            if nodo_actual.data == data_buscada:
                return True
            nodo_actual = nodo_actual.next
        return False

    def eliminar(self, data_a_eliminar):
        nodo_actual = self.head
        nodo_previo = None

        if nodo_actual is not None and nodo_actual.data == data_a_eliminar:
            self.head = nodo_actual.next
            nodo_actual = None
            return

        while nodo_actual is not None and nodo_actual.data != data_a_eliminar:
            nodo_previo = nodo_actual
            nodo_actual = nodo_actual.next

        if nodo_actual is None:
            return

        nodo_previo.next = nodo_actual.next
        nodo_actual = None

if __name__ == "__main__":
    mi_lista = ListaEnlazada()
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