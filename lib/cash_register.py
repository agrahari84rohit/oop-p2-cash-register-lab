#!/usr/bin/env python3


class CashRegister:
    """Track purchases, discounts, and transaction history."""

    def __init__(self, discount=0):
        # Start the register with a 0% discount unless the caller provides one.
        self._discount = 0
        # Use the property setter so the discount is validated immediately.
        self.discount = discount
        # Total starts at zero and grows as items are added.
        self.total = 0
        # Keep a list of purchased item names for display and reporting.
        self.items = []
        # Keep a record of every transaction so we can undo the most recent one.
        self.previous_transactions = []

    @property
    def discount(self):
        # Return the current discount percentage for the register.
        return self._discount

    @discount.setter
    def discount(self, value):
        # Only allow whole-number discounts between 0 and 100 inclusive.
        if isinstance(value, int) and 0 <= value <= 100:
            self._discount = value
        else:
            # Tell the user the discount value is invalid.
            print("Not valid discount")
            self._discount = 0

    def add_item(self, item, price, quantity=1):
        # Increase the running total by the item price times the quantity sold.
        self.total += price * quantity

        # Keep the item names in the register so the customer order is visible.
        self.items.extend([item] * quantity)
        # Save this transaction so it can be undone later if needed.
        self.previous_transactions.append({
            "item": item,
            "price": price,
            "quantity": quantity,
        })

    def apply_discount(self):
        # If the discount is still 0, there is no percentage to apply.
        if self.discount == 0:
            print("There is no discount to apply.")
            return

        # Calculate how much money the discount removes from the current total.
        discount_amount = self.total * (self.discount / 100)
        self.total -= discount_amount

        # Format the discounted total for the user-facing message.
        discounted_total = round(self.total, 2)
        if discounted_total == int(discounted_total):
            print(f"After the discount, the total comes to ${int(discounted_total)}.")
        else:
            print(f"After the discount, the total comes to ${discounted_total:.2f}.")

    def void_last_transaction(self):
        # No transaction history means there is nothing to remove.
        if not self.previous_transactions:
            print("There is no transaction to void.")
            return

        # Undo the most recent addition to the total and item list.
        last_transaction = self.previous_transactions.pop()
        quantity = last_transaction["quantity"]
        self.total -= last_transaction["price"] * quantity

        for _ in range(quantity):
            if self.items:
                self.items.pop()
