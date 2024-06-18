Hosted Here ----> https://django-expensetracker.up.railway.app

# **Expense Tracker**

## **Overview**

The Budget and Expenses Management System is a web application built with Django, using class-based views. It allows users to manage their expenses and budgets efficiently. The main features include tracking expenses, managing budgets, and adding custom categories for better organization.

## **Features**

### **Home Page**
- Displays two tables: one with all expenses and another with all budgets.
- Shows the sum of expenses from the last month at the top.

### **Budget Management**

- Lists all budgets on the budget page.
- Clicking on a budget shows detailed information about that budget.
- In budget details, users can add categories and set maximum values for them.
- Expenses can be assigned to a category, and the system will track if the expenses exceed the set limit for each category.

### **Expenses Management**
- Users can add new expenses, including a value and category.
- Displays all expenses in a datatable format.

### **Profile Management**
- Users can change their username, email, and password.
- Allows adding custom categories for expenses and budget expenses.

### **Additional Features**
- CRUD (Create, Read, Update, Delete) functionality for managing budgets and expenses.
- Test coverage for all views and URLs used in the project to ensure stability.

### **Technologies Used**
- Django: The web framework used for backend development.
- Bootstrap 5: Frontend framework for styling and layout.
- PostgreSQL: Database management system for storing data.
- Django Class-Based Views: Used for managing views in a structured and reusable manner.

### **Usage**
- Home Page: View all expenses and budgets, and see the total expenses for the last month.
- Budget Management: Navigate to the budget page to see all budgets. Click on a budget to view details, add categories, and set maximum values.
- Expenses Management: Add new expenses and assign them to categories. View all expenses in a datatable.
- Profile Management: Change your username, email, and password. Add custom categories for better expense management.

### **Test Suite**
- Tests are written for all views and URLs to ensure functionality and stability.
- The test suite includes validation for adding, deleting, and updating budgets and expenses.
