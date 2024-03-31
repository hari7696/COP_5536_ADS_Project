class AVLNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if not node:
            return AVLNode(key, value)
        elif key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            # Update the value if the key already exists
            node.value = value
            return node

        # Update height and balance the tree
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        return self.balance(node)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node
        elif key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                # Find the in-order successor
                temp = self.min_value_node(node.right)
                node.key = temp.key
                node.value = temp.value
                node.right = self._delete(node.right, temp.key)

        # Update height and balance the tree
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        return self.balance(node)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node or node.key == key:
            return node
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def balance(self, node):
        balance_factor = self.get_balance(node)
        if balance_factor > 1:
            if self.get_balance(node.left) < 0:
                node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        elif balance_factor < -1:
            if self.get_balance(node.right) > 0:
                node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        return node

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        self.update_height(z)
        self.update_height(y)
        return y

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update_height(y)
        self.update_height(x)
        return x

    def min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def inorder_traversal(self, node, result):
        if node:
            self.inorder_traversal(node.left, result)
            result.append(node.value)
            self.inorder_traversal(node.right, result)

    def get_inorder_values(self):
        result = []
        self.inorder_traversal(self.root, result)
        return result
    

class Order:
    def __init__(self, order_id, created_at, value, delivery_time, priority, eta):
        self.order_id = order_id
        self.created_at = created_at
        self.value = value
        self.delivery_time = delivery_time
        self.priority = priority
        self.eta = eta

    def __str__(self):
        return f"Order ID: {self.order_id}, Priority: {self.priority}, ETA: {self.eta}"

class OrderSystem:
    def __init__(self):
        self.priority_tree = AVLTree()
        self.eta_tree = AVLTree()
        self.orders = {}
        self.current_time = 0

    def create_order(self, order_id, current_system_time, order_value, delivery_time):
        self.current_time = current_system_time
        priority = 0.3 * (order_value / 50) - 0.7 * current_system_time
        eta = current_system_time + delivery_time

        last_order = self.find_last_order_before_eta(eta)
        if last_order:
            eta = max(eta, last_order.eta + last_order.delivery_time)

        new_order = Order(order_id, current_system_time, order_value, delivery_time, priority, eta)
        self.orders[order_id] = new_order
        self.priority_tree.insert(priority, new_order)
        self.eta_tree.insert(eta, new_order)

        print(f"Order {order_id} has been created - ETA: {eta}")
        self.print_stats()

        self.deliver_orders()

        delivery_sequence = [order.order_id for order in sorted(self.orders.values(), key=lambda o: o.eta)]
        print(f"Order {order_id} will be delivered after {delivery_sequence.index(order_id)} orders")

    def deliver_orders(self):
        while self.eta_tree.root and self.eta_tree.root.key <= self.current_time:
            min_order = self.find_min_eta(self.eta_tree.root)
            print(f"Order {min_order.order_id} has been delivered at time {self.current_time}")
            self.eta_tree.delete(min_order.eta)
            self.priority_tree.delete(min_order.priority)
            del self.orders[min_order.order_id]

    def find_min_eta(self, node):
        current = node
        while current.left:
            current = current.left
        return current.value

    def find_last_order_before_eta(self, eta):
        suitable_orders = [order for order in self.orders.values() if order.eta < eta]
        return max(suitable_orders, key=lambda o: o.priority) if suitable_orders else None

    def cancel_order(self, order_id):
        if order_id in self.orders:
            order_to_cancel = self.orders.pop(order_id)
            self.priority_tree.delete(order_to_cancel.priority)
            self.eta_tree.delete(order_to_cancel.eta)
            print(f"Order {order_id} has been canceled")
            self.print_stats()

            for order in self.orders.values():
                if order.priority < order_to_cancel.priority:
                    self.recalculate_etas(order)

    def recalculate_etas(self, order):
        prev_order = self.find_last_order_before_eta(order.eta)
        if prev_order:
            order.eta = max(order.created_at, prev_order.eta + prev_order.delivery_time) + order.delivery_time
            self.eta_tree.delete(order.eta)
            self.eta_tree.insert(order.eta, order)
            print(f"Updated ETA: Order {order.order_id} - ETA: {order.eta}")

    def print_orders(self):
        print("Current Orders:")
        for order in self.orders.values():
            print(order)

    def print_stats(self):
        print("Priority Tree Contents:", self.priority_tree.get_inorder_values())
        print("ETA Tree Contents:", self.eta_tree.get_inorder_values())
        print("Orders List:", [(order.order_id, order.priority, order.eta) for order in self.orders.values()])
        print("Current Time:", self.current_time)






# Example usage
order_system = OrderSystem()
order_system.create_order(101, 2, 300, 4)
order_system.create_order(102, 3, 600, 3)
order_system.create_order(103, 7, 200, 2)
order_system.create_order(104, 8, 500, 3)
order_system.cancel_order(102)
order_system.create_order(105, 10, 300, 4)
order_system.print_orders()
