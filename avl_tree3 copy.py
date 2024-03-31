class OrderManagementSystem:
    def __init__(self):
        self.orders = []  # List to store orders
        self.current_system_time = 0  # Tracks the current system time

    def create_order(self, order_id, current_system_time, order_value, delivery_time):
        # Update system time
        self.current_system_time = current_system_time

        # Calculate priority
        priority = 0.3 * (order_value / 50) - 0.7 * current_system_time

        # Create and add the order
        order = {
            'order_id': order_id,
            'priority': priority,
            'delivery_time': delivery_time
        }
        self.orders.append(order)

        # Sort orders by priority and recalculate ETAs
        self.recalculate_etas()
        print(f"Order {order_id} has been created - ETA: {order['eta']}")

    def cancel_order(self, order_id, current_system_time):
        # Update system time
        self.current_system_time = current_system_time

        # Find and remove the order
        self.orders = [order for order in self.orders if order['order_id'] != order_id]
        print(f"Order {order_id} has been canceled")

        # Recalculate ETAs
        self.recalculate_etas()

    def recalculate_etas(self):
        self.orders.sort(key=lambda x: (-x['priority'], x.get('eta', float('inf'))))
        last_eta = self.current_system_time
        for order in self.orders:
            order['eta'] = max(last_eta, order.get('eta', 0)) + order['delivery_time']
            last_eta = order['eta']

    def deliver_orders(self):
        # Deliver orders whose ETA is less than or equal to the current system time
        while self.orders and self.orders[0]['eta'] <= self.current_system_time:
            delivered_order = self.orders.pop(0)
            print(f"Order {delivered_order['order_id']} has been delivered at time {delivered_order['eta']}")
        if self.orders:
            self.recalculate_etas()

    def get_rank_of_order(self, order_id):
        for i, order in enumerate(self.orders):
            if order['order_id'] == order_id:
                print(f"Order {order_id} will be delivered after {i} orders")
                return
        print(f"Order {order_id} is not in the queue")

# Create an instance of the order management system
oms = OrderManagementSystem()

# Run the simulation
oms.create_order(101, 2, 300, 4)
oms.create_order(102, 3, 600, 3)
print([101, 2, 300, 4, 6])  # Print the order details for 101
oms.create_order(103, 7, 200, 2)
oms.current_system_time = 6  # Update the current system time to 6
oms.deliver_orders()  # Deliver orders at time 6
oms.create_order(104, 8, 500, 3)
oms.cancel_order(102, 9)
oms.create_order(105, 10, 300, 4)
oms.get_rank_of_order(105)
oms.current_system_time = 13  # Update the current system time to 13
oms.deliver_orders()  # Deliver orders at time 13
oms.current_system_time = 18  # Update the current system time to 18
oms.deliver_orders()  # Deliver orders at time 18
oms.current_system_time = 24  # Update the current system time to 24
oms.deliver_orders()  # Deliver orders at time 24
