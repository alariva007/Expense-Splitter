def get_participants():
  participants = []
  num_participants = int(input("Enter the number of participants: "))
  for i in range(num_participants):
      name = input(f"Enter the name of participant {i+1}: ")
      participants.append(name)
  return participants

def get_expenses():
  expenses = []
  num_expenses = int(input("Enter the number of expenses: "))
  for i in range(num_expenses):
      description = input(f"Enter the description for expense {i+1}: ")
      amount = float(input(f"Enter the amount for expense {i+1}: "))
      expenses.append({"description": description, "amount": amount})
  return expenses

def calculate_shares(participants, expenses):
  total_amount = sum(expense['amount'] for expense in expenses)
  share_per_person = total_amount / len(participants)
  return total_amount, share_per_person

def display_summary(participants, expenses, total_amount, share_per_person):
  print("\nExpense Summary:")
  print(f"Total Amount: ${total_amount:.2f}")
  print(f"Each participant should contribute: ${share_per_person:.2f}")
  print("\nDetailed Expenses:")
  for expense in expenses:
      print(f"{expense['description']}: ${expense['amount']:.2f}")

def save_summary(participants, expenses, total_amount, share_per_person):
  with open("expense_summary.txt", "w") as file:
      file.write("Expense Summary:\n")
      file.write(f"Total Amount: ${total_amount:.2f}\n")
      file.write(f"Each participant should contribute: ${share_per_person:.2f}\n")
      file.write("\nDetailed Expenses:\n")
      for expense in expenses:
          file.write(f"{expense['description']}: ${expense['amount']:.2f}\n")
  print("\nSummary saved to expense_summary.txt")

def main():
  participants = get_participants()
  expenses = get_expenses()
  total_amount, share_per_person = calculate_shares(participants, expenses)
  display_summary(participants, expenses, total_amount, share_per_person)
  save_summary(participants, expenses, total_amount, share_per_person)

if __name__ == "__main__":
  main()
