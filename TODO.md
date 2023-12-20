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
- add blur on header when scroll-y != 0
- web chat: send data on button "Enter"
- user dropdown blur on scroll
- create mask for email/phone on edit routes

# Chat
- email verification
- fix default user image
- round price on the python side
- footer with home, subscriptions, cart

# Testing database
- add a cli command to set events pictures


# Pagar.me
- how to get checkout url to redirect a user to pagar.me payment form
- what is the format for payload = {"birthdate": "mm/dd/aaa"}
- in the order creation example not mentioned how to add payload, but mentioned that required fields are: customer, customer_id, items, payments