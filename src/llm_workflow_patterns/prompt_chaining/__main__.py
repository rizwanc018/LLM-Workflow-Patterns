from .prompt_chaining import process_support_ticket

user_input = "I was charged ₹25,000 for my order, but the order has been stuck on payment pending for two days. I need this resolved immediately."

result = process_support_ticket(user_input)
print(result)
