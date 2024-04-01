from avl_tree_implementation import AVLTree
import copy

class Ordersystem:

    """
    Class representing an order management system.
    """

    def __init__(self, file):
        
        """
        Initialize the order management system.

        Attributes:
        - priority_avl: AVLTree object representing the AVL tree for order priorities with ETA as key.
        - orders_avl: AVLTree object representing the AVL tree for orders with all meta information.
        - current_system_time: Current system time.
        - first_order: Boolean indicating if it's the first order in the system.
        - driver_return_time: Time when the driver is expected to return.
        - last_order_eta: ETA of the last order.
        """
        self.priority_avl = AVLTree()
        self.orders_avl = AVLTree()
        self.current_system_time = 0
        self.first_order = True
        self.driver_return_time = 0
        self.last_order_eta = 0
        self.f = file

        

    def func_check_order_deliveries(self):

        """
        Check and update the status of order deliveries.

        This function checks if any orders can be marked delivered based on current system time which is obtained from the orders created
        and updates the AVL trees accordingly.
        """

        temp_lst_dict = self.priority_avl.getReverseSortedItems()
        temp_lst = list(temp_lst_dict.values())
        for item in temp_lst:
            
            if self.orders_avl.getNode(self.orders_avl.root, item)['eta'] < self.current_system_time:
                #deleting the key from the dictionary
                self.f.write(f"Order {item} has been delivered at time {self.orders_avl.getNode(self.orders_avl.root, item)['eta']}\n")
                self.orders_avl.root = self.orders_avl.delete(self.orders_avl.root, item)
                self.priority_avl.root = self.priority_avl.delete(self.priority_avl.root, list(temp_lst_dict.keys())[list(temp_lst_dict.values()).index(item)])

    def func_update_eta(self, order_id):

        """
        Update the estimated time of arrival (ETA) for orders.

        Args:
        - order_id: The ID of the order to update the ETA for.

        This function updates the ETA for all orders available before the driver return from last delivery,
        in the AVL trees based on their priority and delivery time.
        If a specific order ID is provided, it also prints the ETA for that order and any updated ETAs for other orders.
        """

        #tmp_orders_priority_dict = 
        # sorted dictionary given by avl tree, gaurantted upto 10k keys then best effort
        #wierd = self.priority_avl.getReverseSortedItems()
        tmp_orders_priority = list(self.priority_avl.getReverseSortedItems().values())
        for item in tmp_orders_priority:
            if self.orders_avl.getNode(self.orders_avl.root, item)['out_for_delivery']:
                tmp_orders_priority.remove(item)

        temp_old_dict = copy.deepcopy(self.orders_avl.getSortedItems())
        # recaulculate the eta for all the orders
        if len(tmp_orders_priority) >= 1:
            item = tmp_orders_priority[0]
            node = copy.deepcopy(self.orders_avl.getNode(self.orders_avl.root, item))
            updated_eta = max(node['creation_time'], self.driver_return_time) \
                                            + node['delivery_time']
            
            #updating the node with new eta 
            node['eta'] = updated_eta
            self.orders_avl.root = self.orders_avl.update(self.orders_avl.root, item, node)

            for item in tmp_orders_priority[1:]:

                previous_itm = tmp_orders_priority[tmp_orders_priority.index(item) - 1]
                previous_node = copy.deepcopy(self.orders_avl.getNode(self.orders_avl.root, previous_itm))
                current_node = copy.deepcopy(self.orders_avl.getNode(self.orders_avl.root, item))
                
                current_node['eta'] = max(
                    current_node['creation_time'], previous_node['eta'] + previous_node['delivery_time']
                ) + current_node['delivery_time']
                
                #updating the node with new_eta
                self.orders_avl.root = self.orders_avl.update(self.orders_avl.root, item, current_node)

        updated_etas = []

        if order_id != -100:
            self.f.write("Order {} has been created - ETA: {}\n".format(order_id, self.orders_avl.getNode(self.orders_avl.root, order_id)['eta']))

        tmp_orders_priority.remove(order_id) if order_id != -100 else None
        for item in tmp_orders_priority:

            if self.orders_avl.getNode(self.orders_avl.root, item)['eta'] != temp_old_dict[item]['eta']:
                updated_etas.append("{}:{}".format(item, self.orders_avl.getNode(self.orders_avl.root, item)['eta']))
        
        if len(updated_etas) > 0:

            self.f.write("Updated ETAs: [{}]\n".format(",".join(updated_etas )))

    def func_create_order(self, order_id, creation_time, order_value, delivery_time):

        """
        Create a new order.

        Args:
        - order_id: The ID of the order.
        - creation_time: The time when the order was created.
        - order_value: The value of the order.
        - delivery_time: The time it takes to deliver the order.

        This function creates a new order and updates the AVL trees accordingly.
        It also checks whether the driver returned from last delivery and pushes new order out for delivery accordingly.
        """

        self.current_system_time = creation_time        
        priority = round(0.3 * (order_value / 50) - 0.7 * creation_time, 4)

        if self.first_order:
            self.first_order = False
            eta = creation_time + delivery_time
            out_for_delivery = True
            self.driver_return_time = eta + delivery_time
            self.last_order_eta = eta
            self.f.write("Order {} has been created - ETA: {}\n".format(order_id, eta))

            new_value = {'creation_time': creation_time, 
                                'order_value': order_value, 
                                'delivery_time': delivery_time, 
                                'priority': priority, 
                                'eta': eta, 
                                'out_for_delivery': out_for_delivery}
            
            self.priority_avl.root = self.priority_avl.insert(self.priority_avl.root, priority, order_id)
            self.orders_avl.root = self.orders_avl.insert(self.orders_avl.root, order_id, new_value)
            
            #temp = self.orders_avl.getSortedItems()
            

        else:
            #last_order_in_list = -100 #self.orders_priority[-1]
            #last_order_eta = -100 #self.orders_dict[last_order_in_list]['eta'] + self.orders_dict[last_order_in_list]['delivery_time']
            eta = -100#max(creation_time , last_order_eta) + 1
            out_for_delivery = False


            new_value = {'creation_time': creation_time, 
                                'order_value': order_value, 
                                'delivery_time': delivery_time, 
                                'priority': priority, 
                                'eta': eta, 
                                'out_for_delivery': out_for_delivery}
            
            self.orders_avl.root = self.orders_avl.insert(self.orders_avl.root, order_id, new_value)
            self.priority_avl.root = self.priority_avl.insert(self.priority_avl.root, priority, order_id)
            
            # queue all orders untill the driver returns
            #temp = self.orders_avl.getSortedItems()
            #self.orders_priority.sort(key=lambda x: self.orders_avl.getSortedItems()[x]['priority'], reverse=True)
            self.func_update_eta(order_id)
            
            self.func_check_order_deliveries()

            # PUSHING ORDERS FOR DELIVERY
            if self.current_system_time > self.driver_return_time and self.priority_avl.getNumberOfNodes() >= 1:
                
                next_order = list(self.priority_avl.getReverseSortedItems().values())[0]
                node = copy.deepcopy(self.orders_avl.getNode(self.orders_avl.root, next_order))
                node['out_for_delivery'] = True
                self.driver_return_time = node['eta'] + node['delivery_time']
                self.last_order_eta = node['eta']
                self.orders_avl.root = self.orders_avl.update(self.orders_avl.root, next_order, node)

        #print ETAs of all orders
        self.func_print_eta()

    def func_cancel_order(self, order_id, current_system_time):

        """
        Cancel an existing order.

        Args:
        - order_id: The ID of the order to cancel.
        - current_system_time: The current system time.

        This function cancels an existing order only if its not out for delivery.
        It check for the field out_for_delivery and relays messages accordingly.
        If it doesnt the find the order in the AVL tree, it relays the message "order already been delivered" accordingly.
        It also checks for order deliveries and updates the ETAs if necessary.
        """

        if self.orders_avl.getNode(self.orders_avl.root, order_id) is None:
            self.f.write(f"Cannot cancel. Order {order_id} has already been delivered.\n")

        elif self.orders_avl.getNode(self.orders_avl.root, order_id)['out_for_delivery']:
            self.f.write(f"Order {order_id} is out for delivery\n")

        elif not self.orders_avl.getNode(self.orders_avl.root, order_id)['out_for_delivery']:
            self.f.write(f"Order {order_id} has been canceled\n")
            self.orders_avl.root = self.orders_avl.delete(self.orders_avl.root, order_id)

            temp_orders_dict = self.priority_avl.getReverseSortedItems()
            self.priority_avl.root = self.priority_avl.delete(self.priority_avl.root, list(temp_orders_dict.keys())[list(temp_orders_dict.values()).index(order_id)] )
            self.func_update_eta(-100)

        self.func_print_eta()

    def func_update_time(self, order_id, current_system_time, new_delivery_time):

        """
        Update the delivery time of an existing order.

        Args:
        - order_id: The ID of the order to update.
        - current_system_time: The current system time.
        - new_delivery_time: The new delivery time for the order.

        This function updates the delivery time of an existing order and updates the AVL trees accordingly, only if the order is not out for delivery.
        It also checks for order deliveries and updates the ETAs if necessary.
        """
        
        if self.orders_avl.getNode(self.orders_avl.root, order_id) is None:
            self.f.write(f"Order {order_id} has already been delivered\n")
        elif self.orders_avl.getNode(self.orders_avl.root, order_id)['out_for_delivery']:
            self.f.write(f"Order {order_id} is out for delivery\n")
        elif not self.orders_avl.getNode(self.orders_avl.root, order_id)['out_for_delivery']:
            
            temp_old_dict = copy.deepcopy(self.orders_avl.getSortedItems())
            update_flg = False

            orders_priority = list(self.priority_avl.getReverseSortedItems().values())

            for item in orders_priority:
                if item == order_id:
                    node = copy.deepcopy(self.orders_avl.getNode(self.orders_avl.root, item))
                    node['eta'] = node['eta'] - node['delivery_time'] + new_delivery_time
                    node['delivery_time'] = new_delivery_time
                    self.orders_avl.root = self.orders_avl.update(self.orders_avl.root, item, node)
                    update_flg = True
                elif update_flg:
                    prev_order = orders_priority[orders_priority.index(item)-1]
                    prev_node = self.orders_avl.getNode(self.orders_avl.root, prev_order)
                    current_node = copy.deepcopy(self.orders_avl.getNode(self.orders_avl.root, item))
                    current_node['eta'] = prev_node['eta'] + prev_node['delivery_time'] + current_node['delivery_time']
                    self.orders_avl.root = self.orders_avl.update(self.orders_avl.root, item, current_node)
                    #self.orders_dict[item]['delivery_time'] = new_delivery_time
            # you will just update the ETA, priorrity will remain the same
            # self.orders_priority.sort(key=lambda x: self.orders_dict[x]['priority'], reverse=True)

            lst_up_eta = []
            for item in orders_priority:
                if self.orders_avl.getNode(self.orders_avl.root, item)['eta'] != temp_old_dict[item]['eta']:
                    lst_up_eta.append("{}:{}".format(item, self.orders_avl.getNode(self.orders_avl.root, item)['eta']))

            if len(lst_up_eta) > 0:
                self.f.write("Updated ETAs: [{}]\n".format(",".join(lst_up_eta )))

        self.func_print_eta()

    def func_double_print(self, time1, time2):
        """
        Prints the orders within the specified time range.

        Args:
            time1 (int): The lower bound of the time range.
            time2 (int): The upper bound of the time range.

        Returns:
            None

        Prints:
            - The list of orders within the specified time range which WILL BE delivered but the delivered orders are not printed.
            - "There are no orders in that time period" if there are no orders in the time range.
        """
        temp = []
        for item in self.priority_avl.getReverseSortedItems().values():
            node = self.orders_avl.getNode(self.orders_avl.root, item)
            if node['eta'] >= time1 and node['eta'] <= time2:
                temp.append(item)
        if len(temp) > 0:
            self.f.write( "[" + ",".join(map(str, temp)) + "]")
            self.f.write("\n")
        else:
            self.f.write("There are no orders in that time period\n")


    def func_print_eta(self):
        """
        Prints the eta (estimated time of arrival) for each item in the AVL tree.

        This method iterates over the items in the AVL tree and prints the item name
        along with its corresponding eta value. The eta value is retrieved from the
        AVL tree node using the `orders_avl` attribute.

        Note:
        - If the `DEBUG` flag is set to True, the method will print the eta values.
        - If the `DEBUG` flag is set to False, the method will do nothing.

        Example usage:
        ```
        tree = AVLTree()
        tree.func_print_eta()
        ```

        """
        DEBUG = False
        if DEBUG:
            tmp_str = ''
            for item in self.orders_avl.getSortedItems():
                tmp_str = tmp_str +  " {}:{} | ".format(item, self.orders_avl.getNode(self.orders_avl.root,item)['eta'])
            self.f.write("\n--------------------")
            self.f.write(tmp_str)
            self.f.write("--------------------\n")
        else:
            pass

    def func_single_print(self, order_id):

        """
        Print the details of a single order.
        """

        if order_id in self.orders_avl.getSortedItems():
            node = self.orders_avl.getNode(self.orders_avl.root, order_id)
            self.f.write( "[" + ",".join( map(str, [order_id, node['creation_time'],
                    node['order_value'],
                      node['delivery_time'],
                         node['eta']])) + "]")
            self.f.write("\n")
        else:
            self.f.write("dude you have the deleted the info\n")

    def func_get_rak_of_order(self, order_id):
        
        """
        Get the rank of an order in the AVL tree for the given order_id.
        """

        lst_orders = list(self.priority_avl.getReverseSortedItems().values())
        if order_id in lst_orders:
            self.f.write("Order {} will be delivered after {} orders.\n".format(order_id, lst_orders.index(order_id)))
        else:
            #self.f.write("Order not found")
            pass

    def func_deliver_remainig_orders(self):

        """ Once the program recieves quit command, it delivers all the remaining orders in the AVL tree """

        lst_orders = list(self.priority_avl.getReverseSortedItems().values())
        for item in lst_orders:
            self.f.write(f"Order {item} has been delivered at time {self.orders_avl.getNode(self.orders_avl.root, item)['eta']}\n")
            #del self.orders_dict[item]




def main(input_filename, output_filename):

    """
    Main function to read the input file and call the respective functions.
    """

    file = open(output_filename, 'w')
    oms =  Ordersystem(file)

    with open(input_filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        command, args = line.split('(')
        args = args[:-1]
        if len(args) > 0:
            args = [int(item) for item in args.split(',')]
        if command == 'createOrder':
            oms.func_create_order(args[0], args[1], args[2], args[3])
        elif command == 'print':
        
            if len(args) == 1:
                oms.func_single_print(args[0])
            else:
                oms.func_double_print(args[0], args[1])

        elif command == 'getRankOfOrder':
            oms.func_get_rak_of_order(args[0])

        elif command == 'updateTime':
            oms.func_update_time(args[0], args[1], args[2])

        elif command == 'cancelOrder':
            oms.func_cancel_order(args[0], args[1])

        elif command == 'Quit':
            oms.func_deliver_remainig_orders()

        else:
            raise ValueError("Invalid command")
    file.close()




if __name__ == "__main__":
    import sys
    #print(sys.argv)
    input_file_name = sys.argv[1]
    output_file = sys.argv[2]
    new_output_file =  'temp_out/' +input_file_name.rstrip(".txt") +'_' + output_file
    main(input_file_name, new_output_file)

# oms = Ordersystem()
# oms.func_create_order(1001, 1, 200, 3)
# oms.func_create_order(1002, 3, 250, 6)
# oms.func_create_order(1003, 8, 100, 3)
# oms.func_create_order(1004, 13, 100, 5)
# oms.func_double_self.f.write(2, 15)
# oms.func_update_time(1003, 15, 1)
# oms.func_create_order(1005, 30, 300, 3)
# oms.func_deliver_remainig_orders()
    
# oms = Ordersystem()
# oms.func_create_order(101, 2, 300, 4)
# oms.func_create_order(102, 3, 600, 3)
# oms.func_single_self.f.write(101)
# oms.func_create_order(103, 7, 200, 2)
# oms.func_create_order(104, 8, 500, 3)
# oms.func_cancel_order(102, 9)
# oms.func_create_order(105, 10, 300, 4)
# oms.func_get_rak_of_order(105)
# oms.func_deliver_remainig_orders()