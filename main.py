import os
import json

class GroceryStore:
    products = {'milk':25,'bread':15,'eggs':12,'butter':45,'apple':18,'mango':50,'banana':12,'grapes':20,'tomato':40,'potato':50,'onion':100}

    def __init__(self,filename='01_projects/03_Grocery_Store_Billing_System_Project/cart.json'):
        self.filename = filename
        self.load_cart()
    
    def load_cart(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename,'r') as file:
                    self.cart = json.load(file)
            
            except json.JSONDecodeError:
                print("\nCorrupted task file. Starting fresh")
        
        else:
            self.cart = {}
    
    def save_cart(self):
        try:
            with open(self.filename,'w') as file:
                json.dump(self.cart,file,indent=4)

        except Exception as e:
            print(f"Error while saving cart: {e}")

    def show_products(self):
        print("\n🛍️ Available Products and Prices:")
        print("Here are the items you can add to your cart:\n")
        print(f"{'PRODUCT':<12}     {'COST':<6}")
        for product,cost in self.products.items():
            print(f"📦 {product:<12}  💲 {cost:<6}")
    
    def get_valid_quantity(self):
        try:
            quantity = int(input("🔢 Enter amount of products: "))
        
        except ValueError:
            print("Error: Invalid input! Please enter a number.")
            return None
        
        else:
            if quantity < 1:
                print("\n❌ You need to add atleast 1 quantity of product")
                return None
            
            return quantity
    
    def confirm_action(self,message):
        confirm = input(f"{message} (yes/no): ").lower()

        if confirm == 'yes':
            return True
        
        return False
    
    def calc_subtotal(self,product):
        return self.cart[product]*self.products[product]
    
    def is_cart_empty(self):
        return not bool(self.cart)
    
    def is_prod_in_cart(self,product):
        return product in self.cart

    def display_table_header(self):
        print("🛍️ Items in cart: 🛒 ")
        print(f"{'PRODUCT':<12}    |{'QUANTITY':<8}   |{'SUBTOTAL':<6}")

    def display_cart_row(self):
        for product,quantity in self.cart.items():
            subtotal = self.calc_subtotal(product)
            print(f"📦 {product:<12} |#️⃣  {quantity:<8} |💲  {subtotal:<6}")

    def add_item(self,product):
        if self.is_prod_in_cart(product):
            confirm = self.confirm_action(f'{product} already exist in cart.Do you want to add more quantity of product!')

            if not confirm:
                print("Adding more quantity of product cancelled!")
                return
            
            quantity = self.get_valid_quantity()
            if quantity is None:
                return

            self.cart[product] += quantity
            self.save_cart()
            print(f"{quantity} products added to cart!")
        
        else:
            quantity = self.get_valid_quantity()

            if quantity is None:
                return

            self.cart[product] = quantity
            print(f"\n🛒 item: {product}")
            print(f"🛒 Price per piece: {self.products[product]}")
            print(f"🔢 Quantity: {quantity}")
            print(f"💰 Subtotal: {self.calc_subtotal(product)}")
            self.save_cart()
            print(f"\nAdded to cart 🛒  successfully. ✔️")

    def show_cart(self):
        if self.is_cart_empty():
            print("🛒 Cart is empty, please enter products to cart! ❌ ")
            return

        self.display_table_header()
        self.display_cart_row()        

    def remove_item(self,product,quantity):
        if quantity >= self.cart[product]:
            confirm = self.confirm_action("\nAre you sure? Product will be completely removed from cart")
            
            if not confirm:
                print("\nYour cart item is not removed.")
                return
            
            self.cart.pop(product)
            self.save_cart()
            print("Product got removed successfully!")

        elif 0 < quantity < self.cart[product]:
            confirm =self.confirm_action(f"\nAre you sure? You want to remove {quantity} amount of products")

            if not confirm:
                print("\nYour cart item is not removed.")
                return
            
            self.cart[product] -= quantity
            self.save_cart()
            print(f"{quantity} of products removed successfully.")
    
        else:
            print("Please enter valid amount!")

    def calc_total(self):
        if self.is_cart_empty():
            print("\n🛑 The cart is empty.Enter any product to calculate total! 🛑")
            return

        total_cost = 0
        for product in self.cart:
            total_cost += self.calc_subtotal(product)
        
        return total_cost

    def show_receipt(self):
        if self.is_cart_empty():
            print("The cart is empty! Please add some products!")
            return
        
        self.display_table_header()
        self.display_cart_row()
        
        print("-"*40)
        print(f"💰 Total: ₹ {self.calc_total()}")
        print('✔️ Thank you for shopping!')

if __name__ == "__main__":
    billing = GroceryStore()

    while True:
        print("\n1️⃣  Show all products available. 🛍️ ")
        print("2️⃣  Add item to cart 📦")
        print("3️⃣  Show items in cart 🛒")
        print("4️⃣  Remove product form cart.")
        print("5️⃣  Calculate total cost 💰")
        print("6️⃣  Print the receipt 🧾")
        print("7️⃣  To exit from Grocery Store Billing.")

        try:
            user_choice = int(input("\n👉 Please make a choice: "))
        
        except ValueError:
            print("Error: Invalid Input! Please enter a valid number between 1 t0 7.")

        else:
            match user_choice:
                case 1:
                    billing.show_products()

                case 2:
                    product = input("📦 Enter what product you want to add to cart: ").lower()

                    if product not in billing.products:
                        print(f"\n❌ This product is not available. ❌")

                    else:
                        billing.add_item(product)
                        
                case 3:
                    billing.show_cart()

                case 4:
                    if billing.is_cart_empty():
                        print("\n🛑 The cart is empty to remove any product! 🛑")

                    else:
                        product = input("\n📦 Enter which product do want to remove: ").lower()

                        if billing.is_prod_in_cart(product):
                            print(f"Quantity available in cart: {billing.cart[product]}")

                            amount = int(input(f"Enter how much amount of {product} you want to remove: 🔢 "))
                            billing.remove_item(product,amount)

                        else:
                            print(f"📦 Product {product} is not it cart. ❌")

                case 5:
                    total_bill = billing.calc_total()

                    if total_bill:
                        print(f"💰 Total Amount: ₹ {total_bill}")

                case 6:
                    billing.show_receipt()

                case 7:
                    confirm = billing.confirm_action("Are you sure? You want to exit from billing system (yes/no): 🧍")

                    if confirm:
                        print("\nHere is you receipt before exiting billing system\n")
                        billing.show_receipt()
                        print("\nExiting...Good Bye 👋 ")
                        break

                    else:
                        print("\nExiting from Billing System Cancelled.")
                
                case _:
                    print("Please enter Valid input!")