# Payment system actions:

- reserve
- buy
- cancel
- refund
- transfer
- send_to_buyer
- mark_as_paid
- confirm_receive
- mark_as_sold
- mark_as_available
- mark_as_unavailable
- mark_as_in_cart
- delete_from_cart

# Change payment credentials

- ?

# User's model changes

- remove activated field
- add email_verified field
- add phone_verified field
- add activated property (if both verifications)

# Disable twilio after the demo

# Ticket page

- wrong template returning on empty search

# Frontend

- user/profile background change (mobile)
- scrollbar styles for different browsers
- user dropdown blur on scroll
- hide error message after delay
- align header desktop
- web chat: send data on button "Enter"
- user dropdown blur on scroll
- create mask for email/phone on edit routes

# Chat

- add logic to subscribe on event
- round price on the python side
- add check if user activated for buy/sell

# Testing database

- add a cli command to set events pictures

# Pagar.me

- include cases when pagar returns errors
- second route for checkout (if needed)
- user changes: pagar_id, all address fields, username property

# Pagar.me questions

- why we are using not sk\_... key but something interim
- how to get checkout url to redirect a user to pagar.me payment form
- where and when we pass metadata
- how to get all customers (the method doesn't work)
