import copy

class Ordersystem:

    def __init__(self):
        self.orders_dict = {}
        self.orders_priority = []
        self.current_system_time = 0
        self.first_order = True
        self.driver_return_time = 0
        self.last_order_eta = 0

    def func_check_order_deliveries(self):

        temp_lst = self.orders_priority.copy()
        for item in temp_lst:
            if self.orders_dict[item]['eta'] < self.current_system_time:
                #deleting the key from the dictionary
                print(f"Order {item} has been delivered at time {self.orders_dict[item]['eta']}")
                del self.orders_dict[item]
                self.orders_priority.remove(item)

    def func_update_eta(self, order_id):

        tmp_orders_priority = self.orders_priority.copy()
        for item in tmp_orders_priority:
            if self.orders_dict[item]['out_for_delivery']:
                tmp_orders_priority.remove(item)

        temp_old_dict = copy.deepcopy(self.orders_dict)
        # recaulculate the eta for all the orders
        if len(tmp_orders_priority) >= 1:
            item = tmp_orders_priority[0]
            self.orders_dict[item]['eta'] = max(self.orders_dict[item]['creation_time'], self.driver_return_time) + self.orders_dict[item]['delivery_time']

            for item in tmp_orders_priority[1:]:
                previous_itm = tmp_orders_priority[tmp_orders_priority.index(item) - 1]
                self.orders_dict[item]['eta'] = max(
                    self.orders_dict[item]['creation_time'], self.orders_dict[previous_itm]['eta'] + self.orders_dict[previous_itm]['delivery_time']
                ) + self.orders_dict[item]['delivery_time']
        
        updated_etas = []

        if order_id != -100:
            print("Order {} has been created - ETA: {}".format(order_id, self.orders_dict[order_id]['eta']))

        tmp_orders_priority.remove(order_id) if order_id != -100 else None
        for item in tmp_orders_priority:
            if self.orders_dict[item]['eta'] != temp_old_dict[item]['eta']:
                updated_etas.append("{}: {}".format(item, self.orders_dict[item]['eta']))
        
        if len(updated_etas) > 0:
            print("Updated ETAs: ", updated_etas )

    def func_create_order(self, order_id, creation_time, order_value, delivery_time):

        self.current_system_time = creation_time        
        priority = 0.3 * (order_value / 50) - 0.7 * creation_time

        if self.first_order:
            self.first_order = False
            eta = creation_time + delivery_time
            out_for_delivery = True
            self.driver_return_time = eta + delivery_time
            self.last_order_eta = eta
            print("Order {} has been created - ETA: {}".format(order_id, eta))

            self.orders_dict[order_id] = {'creation_time': creation_time, 
                                'order_value': order_value, 
                                'delivery_time': delivery_time, 
                                'priority': priority, 
                                'eta': eta, 
                                'out_for_delivery': out_for_delivery}
            self.orders_priority.append(order_id)
            

        else:
            last_order_in_list = -100 #self.orders_priority[-1]
            last_order_eta = -100 #self.orders_dict[last_order_in_list]['eta'] + self.orders_dict[last_order_in_list]['delivery_time']
            eta = -100#max(creation_time , last_order_eta) + 1
            out_for_delivery = False

            self.orders_dict[order_id] = {'creation_time': creation_time, 
                                'order_value': order_value, 
                                'delivery_time': delivery_time, 
                                'priority': priority, 
                                'eta': eta, 
                                'out_for_delivery': out_for_delivery}
            self.orders_priority.append(order_id)
            
            # queue all orders untill the driver returns
            self.orders_priority.sort(key=lambda x: self.orders_dict[x]['priority'], reverse=True)
            self.func_update_eta(order_id)
            
            self.func_check_order_deliveries()

            # PUSHING ORDERS FOR DELIVERY
            if self.current_system_time > self.driver_return_time and len(self.orders_priority) >= 1:
                self.orders_dict[self.orders_priority[0]]['out_for_delivery'] = True
                self.driver_return_time = self.orders_dict[self.orders_priority[0]]['eta'] + self.orders_dict[self.orders_priority[0]]['delivery_time']
                self.last_order_eta = self.orders_dict[self.orders_priority[0]]['eta']

        #print ETAs of all orders
        self.func_print_eta()

    def func_cancel_order(self, order_id, current_system_time):

        if order_id not in self.orders_dict:
            print(f"cannot cancel Order {order_id} has already been delivered")

        elif self.orders_dict[order_id]['out_for_delivery']:
            print(f"Order {order_id} is out for delivery")

        elif not self.orders_dict[order_id]['out_for_delivery']:
            print(f"Order {order_id} has been canceled")
            del self.orders_dict[order_id]
            self.orders_priority.remove(order_id)
            self.func_update_eta(-100)

        self.func_print_eta()

    def func_update_time(self, order_id, current_system_time, new_delivery_time):
        
        if order_id not in self.orders_dict:
            print(f"Order {order_id} has already been delivered")
        elif self.orders_dict[order_id]['out_for_delivery']:
            print(f"Order {order_id} is out for delivery")
        elif not self.orders_dict[order_id]['out_for_delivery']:
            
            temp_old_dict = copy.deepcopy(self.orders_dict)
            update_flg = False
            for item in self.orders_priority:
                if item == order_id:
                    self.orders_dict[item]['eta'] = self.orders_dict[item]['eta'] - self.orders_dict[item]['delivery_time'] + new_delivery_time
                    self.orders_dict[order_id]['delivery_time'] = new_delivery_time
                    update_flg = True
                elif update_flg:
                    prev_order = self.orders_priority[self.orders_priority.index(item)-1]
                    self.orders_dict[item]['eta'] = self.orders_dict[prev_order]['eta'] + self.orders_dict[prev_order]['delivery_time'] + self.orders_dict[item]['delivery_time']
                    #self.orders_dict[item]['delivery_time'] = new_delivery_time
            # you will just update the ETA, priorrity will remain the same
            # self.orders_priority.sort(key=lambda x: self.orders_dict[x]['priority'], reverse=True)

            lst_up_eta = []
            for item in self.orders_priority:
                if self.orders_dict[item]['eta'] != temp_old_dict[item]['eta']:
                    lst_up_eta.append("{}: {}".format(item, self.orders_dict[item]['eta']))

            if len(lst_up_eta) > 0:
                print("Updated ETAs: {}".format(lst_up_eta ))

        self.func_print_eta()

    def func_double_print(self, time1, time2):
        temp = []
        for item in self.orders_priority:
            if self.orders_dict[item]['eta'] >= time1 and self.orders_dict[item]['eta'] <= time2:
                temp.append(item)
        if len(temp)>0:
            print(temp)


    def func_print_eta(self):

        DEBUG = False
        if DEBUG:
            tmp_str = ''
            for item in self.orders_priority:
                tmp_str = tmp_str +  " {}: {} | ".format(item, self.orders_dict[item]['eta'])
            print("\n--------------------")
            print(tmp_str)
            print("--------------------\n")
        else:
            pass

    def func_single_print(self, order_id):
        if order_id in self.orders_dict:
            print([self.orders_dict[order_id]['creation_time'],
                    self.orders_dict[order_id]['order_value'],
                      self.orders_dict[order_id]['delivery_time'],
                         self.orders_dict[order_id]['eta']])
        else:
            print("dude you have the deleted the info")

    def func_get_rak_of_order(self, order_id):
        if order_id in self.orders_priority:
            print("Order {} will be delivered after {} orders".format(order_id, self.orders_priority.index(order_id)))
        else:
            #print("Order not found")
            pass

    def func_deliver_remainig_orders(self):
        for item in self.orders_priority:
            print(f"Order {item} has been delivered at time {self.orders_dict[item]['eta']}")
            #del self.orders_dict[item]

# oms = Ordersystem()
# oms.func_create_order(1001, 1, 200, 3)
# oms.func_create_order(1002, 3, 250, 6)
# oms.func_create_order(1003, 8, 100, 3)
# oms.func_create_order(1004, 13, 100, 5)
# oms.func_double_print(2, 15)
# oms.func_update_time(1003, 15, 1)
# oms.func_create_order(1005, 30, 300, 3)
# oms.func_deliver_remainig_orders()


def main(input_filename):

    oms =  Ordersystem()
    with open(input_filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        command, args = line.split('(')
        args = args[:-1]
        if len(args) > 0:
            args = [int(item) for item in args.split(',')]
        #print(line)
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




if __name__ == "__main__":
    import sys
    input_filename = 'input_file2.txt'#sys.argv[1]
    main(input_filename)

# oms = Ordersystem()
# oms.func_create_order(1001, 1, 200, 3)
# oms.func_create_order(1002, 3, 250, 6)
# oms.func_create_order(1003, 8, 100, 3)
# oms.func_create_order(1004, 13, 100, 5)
# oms.func_double_print(2, 15)
# oms.func_update_time(1003, 15, 1)
# oms.func_create_order(1005, 30, 300, 3)
# oms.func_deliver_remainig_orders()