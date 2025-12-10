class Nodo:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = Nodo(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, current_node, key):
        if key < current_node.key:
            if current_node.left is None:
                current_node.left = Nodo(key)
            else:
                self._insert_recursive(current_node.left, key)
        elif key > current_node.key:
            if current_node.right is None:
                current_node.right = Nodo(key)
            else:
                self._insert_recursive(current_node.right, key)

    def search(self, key):
        path = []
        node = self._search_recursive(self.root, key, path)
        return node is not None, path

    def _search_recursive(self, current_node, key, path):
        if current_node is None:
            return None
        path.append(current_node.key)
        if key == current_node.key:
            return current_node
        elif key < current_node.key:
            return self._search_recursive(current_node.left, key, path)
        else:
            return self._search_recursive(current_node.right, key, path)

    def delete(self, key):
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, root, key):
        if root is None:
            return root
        if key < root.key:
            root.left = self._delete_recursive(root.left, key)
        elif key > root.key:
            root.right = self._delete_recursive(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            
            temp = self._find_min(root.right)
            root.key = temp.key
            root.right = self._delete_recursive(root.right, temp.key)
        return root

    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, root, result):
        if root:
            self._inorder_recursive(root.left, result)
            result.append(root.key)
            self._inorder_recursive(root.right, result)

    def preorder(self):
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, root, result):
        if root:
            result.append(root.key)
            self._preorder_recursive(root.left, result)
            self._preorder_recursive(root.right, result)

    def postorder(self):
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, root, result):
        if root:
            self._postorder_recursive(root.left, result)
            self._postorder_recursive(root.right, result)
            result.append(root.key)

    def height(self):
        return self._height_recursive(self.root)

    def _height_recursive(self, root):
        if root is None:
            return -1
        return 1 + max(self._height_recursive(root.left), self._height_recursive(root.right))

    def size(self):
        return self._size_recursive(self.root)

    def _size_recursive(self, root):
        if root is None:
            return 0
        return 1 + self._size_recursive(root.left) + self._size_recursive(root.right)

    def export_inorder(self, filename):
        try:
            with open(filename, 'w') as f:
                f.write(' '.join(map(str, self.inorder())))
            print(f"Recorrido inorden guardado en '{filename}'")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

def run_console():
    bst = BST()
    
    def display_help():
        print("\nComandos disponibles:")
        print("  insert <número>       - Inserta un número en el árbol.")
        print("  search <número>       - Busca un número y muestra la ruta si existe.")
        print("  delete <número>       - Elimina un número del árbol.")
        print("  inorder               - Muestra el recorrido en orden.")
        print("  preorder              - Muestra el recorrido en preorden.")
        print("  postorder             - Muestra el recorrido en postorden.")
        print("  height                - Muestra la altura del árbol.")
        print("  size                  - Muestra el número de nodos.")
        print("  export <nombre_archivo> - Guarda el recorrido inorden en un archivo.")
        print("  help                  - Muestra esta lista de comandos.")
        print("  exit                  - Sale del programa.\n")

    display_help()

    while True:
        try:
            command = input("BST_Shell> ").strip().split()
            if not command:
                continue
            
            action = command[0].lower()
            
            if action == 'insert':
                if len(command) < 2:
                    print("Uso: insert <número>")
                    continue
                key = int(command[1])
                bst.insert(key)
                print(f"Número {key} insertado.")
            
            elif action == 'search':
                if len(command) < 2:
                    print("Uso: search <número>")
                    continue
                key = int(command[1])
                found, path = bst.search(key)
                if found:
                    print(f"Número {key} encontrado. Ruta: {' -> '.join(map(str, path))}")
                else:
                    print(f"Número {key} no encontrado.")
            
            elif action == 'delete':
                if len(command) < 2:
                    print("Uso: delete <número>")
                    continue
                key = int(command[1])
                initial_size = bst.size()
                bst.delete(key)
                final_size = bst.size()
                if final_size < initial_size:
                    print(f"Número {key} eliminado.")
                else:
                    print(f"Número {key} no se encontró para eliminar.")

            elif action == 'inorder':
                print("Recorrido Inorden:", bst.inorder())
            
            elif action == 'preorder':
                print("Recorrido Preorden:", bst.preorder())

            elif action == 'postorder':
                print("Recorrido Postorden:", bst.postorder())

            elif action == 'height':
                print("Altura del árbol:", bst.height())

            elif action == 'size':
                print("Número de nodos:", bst.size())
                
            elif action == 'export':
                if len(command) < 2:
                    print("Uso: export <nombre_archivo>")
                    continue
                filename = command[1]
                bst.export_inorder(filename)

            elif action == 'help':
                display_help()

            elif action == 'exit':
                print("Saliendo del Gestor de números.")
                break

            else:
                print(f"Comando desconocido: '{action}'. Usa 'help' para ver la lista de comandos.")

        except ValueError:
            print("Entrada inválida. Asegúrate de ingresar un número válido.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    run_console()