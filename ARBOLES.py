import uuid
import json
from collections import deque

class Node:
    def __init__(self, nombre, tipo, contenido=None, parent=None, id=None):
        self.id = id if id else str(uuid.uuid4())
        self.nombre = nombre
        self.tipo = tipo
        self.contenido = contenido
        self.children = {}
        self.parent = parent

    def __repr__(self):
        return f"<{self.tipo.capitalize()} name='{self.nombre}'>"

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.node_ids = set() 

class FileSystem:
    def __init__(self, json_file='fs_data.json'):
        self.json_file = json_file
        self.root = None
        self.trie_root = TrieNode()
        self.node_map = {}
        self.trash_can = {}
        self.current_working_dir = '/'
        
        if self._load_from_json():
            print(f"Sistema de archivos cargado desde {self.json_file}.")
        else:
            print("Inicializando nuevo sistema de archivos.")
            self.root = Node(nombre="/", tipo="carpeta")
            self.node_map[self.root.id] = self.root
            self._insert_name_into_trie(self.root.nombre, self.root.id)

    # DÍA 4: Persistencia
    def _to_serializable(self, node):
        return {
            'id': node.id,
            'nombre': node.nombre,
            'tipo': node.tipo,
            'contenido': node.contenido,
            'children': {name: self._to_serializable(child) 
                         for name, child in node.children.items()}
        }

    def _save_to_json(self):
        try:
            data = {
                'root': self._to_serializable(self.root),
                'trash_can': {id: self._to_serializable(node) for id, node in self.trash_can.items()}
            }
            with open(self.json_file, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar en JSON: {e}")
            return False

    def _rebuild_node(self, data, parent=None):
        node = Node(
            nombre=data['nombre'],
            tipo=data['tipo'],
            contenido=data['contenido'],
            parent=parent,
            id=data['id']
        )
        self.node_map[node.id] = node
        self._insert_name_into_trie(node.nombre, node.id)
        
        for name, child_data in data['children'].items():
            child_node = self._rebuild_node(child_data, parent=node)
            node.children[name] = child_node
        
        return node

    def _load_from_json(self):
        try:
            with open(self.json_file, 'r') as f:
                data = json.load(f)
            
            self.node_map = {}
            self.trie_root = TrieNode()

            self.root = self._rebuild_node(data['root'])
            
            self.trash_can = {}
            for id, trash_data in data['trash_can'].items():
                trash_node = self._rebuild_node(trash_data, parent=None)
                self.trash_can[id] = trash_node

            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False

    # Métodos de Navegación
    def _get_path_parts(self, path):
        return [p for p in path.split('/') if p]

    def _get_node_from(self, start_node, path_parts):
        current = start_node
        for name in path_parts:
            if name not in current.children:
                return None
            current = current.children[name]
        return current

    def get_node_by_path(self, path):
        if path == '/':
            return self.root
        return self._get_node_from(self.root, self._get_path_parts(path))

    def show_full_path(self, node):
        path = deque()
        current = node
        while current and current != self.root:
            path.appendleft(current.nombre)
            current = current.parent
        
        return '/' + '/'.join(path)

    # DÍAS 5-6: Trie y Búsqueda
    def _insert_name_into_trie(self, name, node_id):
        if not name: return

        current = self.trie_root
        for char in name.lower():
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        
        current.is_end_of_word = True
        current.node_ids.add(node_id)

    def _delete_name_from_trie(self, name, node_id):
        if not name: return

        current = self.trie_root
        for char in name.lower():
            if char not in current.children:
                return
            current = current.children[char]
        
        if node_id in current.node_ids:
            current.node_ids.discard(node_id)
            if not current.node_ids:
                current.is_end_of_word = False

    def _find_all_node_ids_from_trie(self, start_node):
        ids = set()
        
        if start_node.is_end_of_word:
            ids.update(start_node.node_ids)
            
        for child in start_node.children.values():
            ids.update(self._find_all_node_ids_from_trie(child))
            
        return ids

    def search_by_prefix(self, prefix):
        prefix = prefix.lower()
        current = self.trie_root
        
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]

        matching_ids = self._find_all_node_ids_from_trie(current)
        
        results = []
        for node_id in matching_ids:
            node = self.node_map.get(node_id)
            if node:
                results.append({
                    'nombre': node.nombre,
                    'ruta': self.show_full_path(node),
                    'tipo': node.tipo
                })
        return results

    # Operaciones de Árbol (Días 2-3)
    def create_node(self, parent_path, nombre, tipo, contenido=None):
        parent_node = self.get_node_by_path(parent_path)

        if not parent_node or parent_node.tipo != 'carpeta' or nombre in parent_node.children:
            print("Error: Ruta padre inválida o el nombre ya existe.")
            return None

        new_node = Node(nombre=nombre, tipo=tipo, contenido=contenido, parent=parent_node)
        parent_node.children[nombre] = new_node
        
        self.node_map[new_node.id] = new_node
        self._insert_name_into_trie(nombre, new_node.id)
        self._save_to_json()
        print(f"Éxito: Creado {tipo} '{nombre}' en '{parent_path}'.")
        return new_node

    def rename_node(self, old_path, new_name):
        node_to_rename = self.get_node_by_path(old_path)
        
        if not node_to_rename or node_to_rename == self.root: 
            print("Error: El nodo no existe o es la raíz.")
            return False
        
        parent_node = node_to_rename.parent
        if new_name in parent_node.children: 
            print(f"Error: Ya existe un nodo llamado '{new_name}' en el directorio padre.")
            return False

        self._delete_name_from_trie(node_to_rename.nombre, node_to_rename.id)
        
        del parent_node.children[node_to_rename.nombre]
        
        node_to_rename.nombre = new_name
        
        parent_node.children[new_name] = node_to_rename
        
        self._insert_name_into_trie(new_name, node_to_rename.id)
        self._save_to_json()
        print(f"Éxito: Renombrado '{old_path}' a '{new_name}'.")
        return True

    def move_node(self, source_path, destination_path):
        node_to_move = self.get_node_by_path(source_path)
        dest_parent = self.get_node_by_path(destination_path)

        if not node_to_move or not dest_parent or dest_parent.tipo != 'carpeta':
            print("Error: Ruta de origen/destino inválida.")
            return False
        
        if node_to_move == self.root:
            print("Error: No se puede mover la raíz.")
            return False
        
        if node_to_move.nombre in dest_parent.children:
            print(f"Error: Ya existe un nodo llamado '{node_to_move.nombre}' en el destino.")
            return False
        
        original_parent = node_to_move.parent
        del original_parent.children[node_to_move.nombre]
        
        node_to_move.parent = dest_parent
        dest_parent.children[node_to_move.nombre] = node_to_move
        
        self._save_to_json()
        print(f"Éxito: Movido '{source_path}' a '{destination_path}'.")
        return True
    
    def delete_node(self, path):
        node_to_delete = self.get_node_by_path(path)

        if not node_to_delete or node_to_delete == self.root:
            print("Error: Nodo no encontrado o es la raíz.")
            return False
        
        self._delete_name_from_trie(node_to_delete.nombre, node_to_delete.id)
        
        original_parent = node_to_delete.parent
        del original_parent.children[node_to_delete.nombre]
        
        node_to_delete.parent = None
        self.trash_can[node_to_delete.id] = node_to_delete

        self._save_to_json()
        print(f"Éxito: Nodo '{path}' movido a la papelera temporal.")
        return True

    def list_children(self, path):
        node = self.get_node_by_path(path)
        if not node or node.tipo != 'carpeta':
            print("Error: Ruta no existe o no es una carpeta.")
            return

        print(f"\nContenido de {path} ({len(node.children)} elementos):")
        children_list = sorted(node.children.values(), key=lambda n: (n.tipo != 'carpeta', n.nombre))
        
        for child in children_list:
            prefix = "📁" if child.tipo == 'carpeta' else "📄"
            print(f"  {prefix} {child.nombre}")

    def export_preorder(self, node):
        result = []
        def _preorder_traverse(current_node):
            full_path = self.show_full_path(current_node)
            result.append(f"[{current_node.tipo.upper()}] {full_path}")
            
            sorted_children = sorted(current_node.children.values(), key=lambda n: n.nombre)
            for child in sorted_children:
                _preorder_traverse(child)

        _preorder_traverse(node)
        
        print("\n--- Recorrido en Preorden ---")
        for item in result:
            print(item)
        print("----------------------------\n")
        return result

    # DÍAS 7-9: Interfaz de Consola
    def change_dir(self, new_path):
        if new_path == '..':
            current_node = self.get_node_by_path(self.current_working_dir)
            if current_node and current_node.parent:
                self.current_working_dir = self.show_full_path(current_node.parent)
                print(f"CWD: {self.current_working_dir}")
                return
            
        target_node = self.get_node_by_path(new_path)
        
        if not target_node:
            print("Error: Directorio no encontrado.")
        elif target_node.tipo != 'carpeta':
            print("Error: El nodo no es un directorio.")
        else:
            self.current_working_dir = self.show_full_path(target_node)
            print(f"CWD: {self.current_working_dir}")

    def get_absolute_path(self, path):
        if path.startswith('/'):
            return path
        
        cwd_parts = self._get_path_parts(self.current_working_dir)
        path_parts = self._get_path_parts(path)
        
        final_parts = []
        
        for part in cwd_parts + path_parts:
            if part == '..':
                if final_parts:
                    final_parts.pop()
            elif part == '.':
                continue
            else:
                final_parts.append(part)

        return '/' + '/'.join(final_parts)

    def run_console(self):
        print("--- FileSystem Shell (Proyecto Árboles) ---")
        print("Comandos: mkdir, touch, ls, cd, mv, rm, rename, search, export, exit")
        
        while True:
            try:
                command_input = input(f"\n{self.current_working_dir} > ").strip()
                if not command_input: continue

                parts = command_input.split()
                cmd = parts[0]
                args = parts[1:]

                if cmd == 'exit':
                    print("Guardando y saliendo...")
                    self._save_to_json()
                    break

                elif cmd == 'mkdir':
                    if len(args) != 1: print("Uso: mkdir <nombre_carpeta>")
                    else: self.create_node(self.current_working_dir, args[0], 'carpeta')
                
                elif cmd == 'touch':
                    if len(args) != 1: print("Uso: touch <nombre_archivo>")
                    else: self.create_node(self.current_working_dir, args[0], 'archivo', content="")

                elif cmd == 'ls':
                    path = self.get_absolute_path(args[0]) if args else self.current_working_dir
                    self.list_children(path)

                elif cmd == 'cd':
                    if not args: print("Uso: cd <ruta>")
                    else: self.change_dir(self.get_absolute_path(args[0]))
                
                elif cmd == 'mv':
                    if len(args) != 2: print("Uso: mv <ruta_origen> <ruta_destino>")
                    else: 
                        source_path = self.get_absolute_path(args[0])
                        dest_path = self.get_absolute_path(args[1])
                        self.move_node(source_path, dest_path)
                
                elif cmd == 'rm':
                    if len(args) != 1: print("Uso: rm <ruta_nodo>")
                    else: self.delete_node(self.get_absolute_path(args[0]))

                elif cmd == 'rename':
                    if len(args) != 2: print("Uso: rename <ruta_nodo> <nuevo_nombre>")
                    else: self.rename_node(self.get_absolute_path(args[0]), args[1])

                elif cmd == 'search':
                    if len(args) != 1: print("Uso: search <prefijo>")
                    else: 
                        results = self.search_by_prefix(args[0])
                        if results:
                            print("\n--- Resultados de Búsqueda (Autocompletado) ---")
                            for res in results:
                                print(f"[{res['tipo'].upper()}] {res['nombre']} -> {res['ruta']}")
                        else:
                            print("No se encontraron coincidencias.")

                elif cmd == 'export':
                    if len(args) != 1 or args[0] != 'preorden':
                        print("Uso: export preorden")
                    else:
                        self.export_preorder(self.root)
                
                else:
                    print(f"Comando desconocido: {cmd}")

            except Exception as e:
                print(f"Error inesperado: {e}")

if __name__ == "__main__":
    fs = FileSystem()
    
    if len(fs.root.children) == 0:
        fs.create_node("/", "Documentos", "carpeta")
        fs.create_node("/Documentos", "Informe_Final.pdf", "archivo")
        fs.create_node("/Documentos", "Borrador", "carpeta")
        fs.create_node("/", "Fotos", "carpeta")
        fs.create_node("/Fotos", "Vacaciones.jpg", "archivo")
        fs._save_to_json()

    fs.run_console()