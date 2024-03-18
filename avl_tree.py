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
    def __init__(self, orderId, currentSystemTime, orderValue, deliveryTime):
        self.orderId = orderId
        self.currentSystemTime = currentSystemTime
        self.orderValue = orderValue
        self.deliveryTime = deliveryTime
        self.priority = self.calculate_priority()
        self.ETA = None

    def calculate_priority(self):
        valueWeight = 0.3
        timeWeight = 0.7
        normalizedOrderValue = self.orderValue / 50
        return valueWeight * normalizedOrderValue - timeWeight * self.currentSystemTime

    def __repr__(self):
        return f"[{self.orderId} {self.currentSystemTime} {self.orderValue} {self.deliveryTime} {self.ETA}]"

class OrderManagementSystem:
    def __init__(self):
        self.priority_tree = AVLTree()
        self.eta_tree = AVLTree()
        self.orders = {}
        self.last_delivered_order_time = 0

    def create_order(self, orderId, currentSystemTime, orderValue, deliveryTime):
        order = Order(orderId, currentSystemTime, orderValue, deliveryTime)
        self.orders[orderId] = order
        self.calculate_eta(order)
        self.priority_tree.insert(order.priority, orderId)
        self.eta_tree.insert(order.ETA, orderId)
        print(f"Order {orderId} has been created - ETA: {order.ETA}")
        self.deliver_orders(currentSystemTime)

    def cancel_order(self, orderId, currentSystemTime):
        if orderId in self.orders:
            order = self.orders[orderId]
            self.priority_tree.delete(order.priority)
            self.eta_tree.delete(order.ETA)
            del self.orders[orderId]
            print(f"Order {orderId} has been canceled")
            self.update_etas()
            self.deliver_orders(currentSystemTime)
        else:
            print(f"Cannot cancel. Order {orderId} has already been delivered or does not exist.")

    def search_order(self, orderId):
        if orderId in self.orders:
            order = self.orders[orderId]
            print(order)
        else:
            print("Order not found")

    def calculate_eta(self, order):
        order.ETA = max(order.currentSystemTime, self.last_delivered_order_time) + order.deliveryTime
        self.last_delivered_order_time = order.ETA + order.deliveryTime

    def update_etas(self):
        self.last_delivered_order_time = 0
        for order in sorted(self.orders.values(), key=lambda o: o.priority):
            old_eta = order.ETA
            self.calculate_eta(order)
            if old_eta != order.ETA:
                self.eta_tree.delete(old_eta)
                self.eta_tree.insert(order.ETA, order.orderId)
                print(f"Updated ETA for Order {order.orderId}: {order.ETA}")

    def deliver_orders(self, currentSystemTime):
        delivered_orders = []
        for eta in sorted(self.eta_tree.get_inorder_values()):
            if eta > currentSystemTime:
                break
            order_id = self.eta_tree.search(eta)
            if order_id:
                print(f"Order {order_id} has been delivered at time {eta}")
                delivered_orders.append(order_id)
        for order_id in delivered_orders:
            order = self.orders[order_id]
            self.eta_tree.delete(order.ETA)
            self.priority_tree.delete(order.priority)
            del self.orders[order_id]

    def print_orders_in_range(self, time1, time2):
        orders_in_range = [order_id for order_id in self.orders if time1 <= self.orders[order_id].ETA <= time2]
        if orders_in_range:
            print(orders_in_range)
        else:
            print("There are no orders in that time period")

    def get_rank_of_order(self, orderId):
        if orderId in self.orders:
            order = self.orders[orderId]
            rank = 0
            for eta in sorted(self.eta_tree.get_inorder_values()):
                if eta >= order.ETA:
                    break
                rank += 1
            print(f"Order {orderId} will be delivered after {rank} orders")
        else:
            print("Order not found")


def main(input_filename):
    oms = OrderManagementSystem()
    with open(input_filename, 'r') as file:
        for line in file:
            command = line.strip().split('(')[0]
            args = line.strip().split('(')[1][:-1].split(',')
            if len(args) > 1:
                args = [arg.strip() for arg in args]
            if command == "createOrder":
                oms.create_order(int(args[0]), int(args[1]), int(args[2]), int(args[3]))
            elif command == "cancelOrder":
                oms.cancel_order(int(args[0]), int(args[1]))
            elif command == "print":
                if len(args) == 1:
                    oms.search_order(int(args[0]))
                else:
                    oms.print_orders_in_range(int(args[0]), int(args[1]))
            elif command == "getRankOfOrder":
                oms.get_rank_of_order(int(args[0]))
            elif command == "Quit":
                break



if __name__ == "__main__":
    import sys
    input_filename = sys.argv[1]
    main(input_filename)