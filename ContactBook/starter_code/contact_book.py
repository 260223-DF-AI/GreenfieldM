# contact_book.py - Contact Book Application
# Starter code for e003-exercise-data-structures

"""
Contact Book Application
------------------------
A simple contact management system using Python data structures.

Data Structure:
- Each contact is a dictionary with: name, phone, email, category, created_at
- All contacts are stored in a list

Complete the TODO sections below to finish the application.
"""

from datetime import datetime

# =============================================================================
# Initialize Contact Book
# =============================================================================
contacts = []


# =============================================================================
# TODO: Task 1 - Create the Contact Book
# =============================================================================

def add_contact(contacts, name, phone, email, category):
    """
    Add a new contact to the contact book.
    
    Args:
        contacts: The list of all contacts
        name: Contact's full name
        phone: Contact's phone number
        email: Contact's email address
        category: One of: friend, family, work, other
    
    Returns:
        The created contact dictionary
    """
    # TODO: Add created_at timestamp using datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # TODO: Create a contact dictionary with all fields
    contact = {
        "name": name,
        "phone": phone,
        "email": email,
        "category": category,
        "created_at": created_at
    }

    # TODO: Append to contacts list
    contacts.append(contact)

    # TODO: Return the new contact
    return contact

    pass

#TESTING STUFF
#add_contact(contacts, "Alice Johnson", "555-123-4567", "alice@example.com", "friend")
#add_contact(contacts, "Bob Smith", "555-987-6543", "bob@work.com", "work")
#add_contact(contacts, "Carol White", "555-456-7890", "carol@family.net", "family")

# =============================================================================
# TODO: Task 2 - Display Contacts
# =============================================================================

def display_all_contacts(contacts):
    """
    Display all contacts in a formatted table.
    
    Output format:
    =============================================
                CONTACT BOOK (X contacts)
    =============================================
    #  | Name            | Phone         | Category
    ---|-----------------|---------------|----------
    1  | Alice Johnson   | 555-123-4567  | friend
    ...
    """
    # TODO: Print header with contact count
    print("=" * 44)
    print(f"        CONTACT BOOK ({len(contacts)} contacts)")
    print("=" * 44)
    # TODO: Print table headers
    print("#   | Name           |Phone          |Category")
    print("----|----------------|---------------|---------")
    # TODO: Loop through contacts and print each row
    for i, contact in enumerate(contacts, start = 1):
        name = contact.get("name")
        phone = contact.get("phone")
        category = contact.get("category")
        for contact in contacts:
            if "category" not in contact:
                contact["category"] = "unknown"
        print(f"{i:<2} | {name:<15} | {phone:<13} | {category}")
    # TODO: Print footer
    print("=" * 44)
    pass


def display_contact_details(contact):
    """
    Display detailed information for a single contact.
    
    Output format:
    --- Contact Details ---
    Name:     [name]
    Phone:    [phone]
    Email:    [email]
    Category: [category]
    Added:    [created_at]
    ------------------------
    """
    # TODO: Print formatted contact details
    print("--- Contact Details ---")
    print(f"Name:     {contact['name']}")
    print(f"Phone:    {contact['phone']}")
    print(f"Email:    {contact['email']}")
    print(f"Category: {contact['category']}")
    print(f"Added:    {contact['created_at']}")
    print("-" * 24)

    pass


# =============================================================================
# TODO: Task 3 - Search Functionality
# =============================================================================

def search_by_name(contacts, query):
    """
    Find contacts whose name contains the query string.
    Case-insensitive search.
    
    Returns:
        List of matching contacts
    """
    # TODO: Filter contacts where query is in name (case-insensitive)
    # Hint: Use list comprehension and .lower()
    return [
        contact for contact in contacts
        if query.lower() in contact["name"].lower()
    ]

    pass


def filter_by_category(contacts, category):
    """
    Return all contacts in a specific category.
    
    Returns:
        List of contacts matching the category
    """
    # TODO: Filter contacts by category
    return [
        contact for contact in contacts
        if contact["category"].lower() == category.lower()
    ]
    pass


def find_by_phone(contacts, phone):
    """
    Find a contact by exact phone number.
    
    Returns:
        The contact dictionary if found, None otherwise
    """
    # TODO: Search for contact with matching phone
    for contact in contacts:
        if contact["phone"] == phone:
            return contact
    return None
    pass


# =============================================================================
# TODO: Task 4 - Update and Delete
# =============================================================================

def update_contact(contacts, phone, field, new_value):
    """
    Update a specific field of a contact.
    
    Args:
        contacts: The list of all contacts
        phone: Phone number to identify the contact
        field: The field to update (name, phone, email, or category)
        new_value: The new value for the field
    
    Returns:
        True if updated, False if contact not found
    """
    # TODO: Find contact by phone
    # TODO: Update the specified field
    # TODO: Return success/failure
    for contact in contacts:
        if contact["phone"] == phone: #find contact by phone
            if field in ["name", "phone", "email", "category"]: #only update specified field
                contact[field] = new_value
                return True #return success/failure
    return False
    pass


def delete_contact(contacts, phone):
    """
    Delete a contact by phone number.
    
    Returns:
        True if deleted, False if not found
    """
    # TODO: Find and remove contact with matching phone
    for i, contact in enumerate(contacts):
        if contact["phone"] == phone:
            contacts.pop(i)
            return True
    return False
    pass


# =============================================================================
# TODO: Task 5 - Statistics
# =============================================================================

def display_statistics(contacts):
    """
    Display statistics about the contact book.
    
    Output:
    --- Contact Book Statistics ---
    Total Contacts: X
    By Category:
      - Friends: X
      - Family: X
      - Work: X
      - Other: X
    Most Recent: [name] (added [date])
    -------------------------------
    """
    # TODO: Count total contacts
    total = len(contacts)

    # TODO: Count contacts by category
    friends = sum(1 for c in contacts if c["category"].lower() == "friend")
    family = sum(1 for c in contacts if c["category"].lower() == "family")
    work = sum(1 for c in contacts if c["category"].lower() == "work")
    other = sum(1 for c in contacts if c["category"].lower() == "other")

    #printing content that i have so far
    print("--- Contact Book Statistics ---")
    print(f"Total Contacts: {total}")
    print("BY CATEGORY: ")
    print(f"    -Friends: {friends}")
    print(f"    -Family:  {family}")
    print(f"    -Work:    {work}")
    print(f"    -Other:   {other}")


    # TODO: Find most recently added contact
    if contacts:
        most_recent = max(
            contacts,
            key = lambda c: datetime.strptime(c["created_at"], "%Y-%m-%d %H:%M:%S")
        )
        print(f"Most Recent: {most_recent['name']} (added {most_recent['created_at']})")
    else:
        print("Most recent: None")

    #printing end
    print("-" * 31)
    pass


# =============================================================================
# STRETCH GOAL: Interactive Menu
# =============================================================================

def display_menu():
    """Display the main menu."""
    print("\n========== CONTACT BOOK ==========")
    print("1. View all contacts")
    print("2. Add new contact")
    print("3. Search contacts")
    print("4. Update contact")
    print("5. Delete contact")
    print("6. View statistics")
    print("0. Exit")
    print("==================================")


def main():
    """Main function with interactive menu."""
    # TODO: Implement menu loop
    # Use while True and break on exit choice
    while True:
        display_menu()
        choice = input("Enter choice: ").strip()

        # Exit
        if choice == "0":
            print("Goodbye!")
            break

        # View all contacts
        elif choice == "1":
            if contacts:
                display_all_contacts(contacts)
            else:
                print("No contacts found.")

        # Add new contact
        elif choice == "2":
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            email = input("Enter email: ")
            category = input("Enter category (friend/family/work/other): ")

            new_contact = add_contact(
                contacts, name, phone, email, category
            )

            print(f"Contact added: {new_contact['name']}")

        # Search contacts
        elif choice == "3":
            print("\nSearch Options:")
            print("1. By Name")
            print("2. By Category")
            print("3. By Phone")

            search_choice = input("Choose search type: ")

            # Search by name
            if search_choice == "1":
                query = input("Enter name to search: ")
                results = search_by_name(contacts, query)

                if results:
                    for c in results:
                        display_contact_details(c)
                else:
                    print("No matches found.")

            # Filter by category
            elif search_choice == "2":
                category = input("Enter category: ")
                results = filter_by_category(contacts, category)

                if results:
                    for c in results:
                        display_contact_details(c)
                else:
                    print("No matches found.")

            # Find by phone
            elif search_choice == "3":
                phone = input("Enter phone: ")
                result = find_by_phone(contacts, phone)

                if result:
                    display_contact_details(result)
                else:
                    print("Contact not found.")

            else:
                print("Invalid search option.")

        # Update contact
        elif choice == "4":
            phone = input("Enter phone of contact to update: ")
            field = input("Field to update (name/phone/email/category): ")
            new_value = input("Enter new value: ")

            success = update_contact(contacts, phone, field, new_value)

            if success:
                print("Contact updated successfully.")
            else:
                print("Contact not found or invalid field.")

        # Delete contact
        elif choice == "5":
            phone = input("Enter phone of contact to delete: ")

            success = delete_contact(contacts, phone)

            if success:
                print("Contact deleted.")
            else:
                print("Contact not found.")

        # View statistics
        elif choice == "6":
            display_statistics(contacts)

        # Invalid option
        else:
            print("Invalid choice. Please try again.")
    pass


# =============================================================================
# Test Code - Add sample data and test functions
# =============================================================================

if __name__ == "__main__":
    print("Contact Book Application")
    print("=" * 40)
    
    # TODO: Add at least 5 sample contacts
    # add_contact(contacts, "Alice Johnson", "555-123-4567", "alice@example.com", "friend")
    add_contact(contacts, "Alice Johnson", "555-123-4567", "alice@example.com", "friend")
    add_contact(contacts, "Bob Smith", "555-987-6543", "bob@work.com", "work")
    add_contact(contacts, "Carol White", "555-456-7890", "carol@family.net", "family")
    add_contact(contacts, "Magan Greenfield", "847-123-4567", "magan@other.org", "other")
    add_contact(contacts, "Haig Hagopian", "847-987-6543", "haig@friend.com", "friend")
    
    # TODO: Test your functions
    display_all_contacts(contacts)
    print()
    results = search_by_name(contacts, "alice")
    print()
    # etc.
    found = find_by_phone(contacts, "555-999-0000")
    print()

    update = update_contact(contacts, "555-222-333", "email", "bob@email.com")
    print("updated?", update)
    display_all_contacts(contacts)
    print()

    delete = delete_contact(contacts, "555-123-4567")
    print("Deleted?", delete)
    display_all_contacts(contacts)
    print()

    display_statistics(contacts)
    print("Done with normal testing!")

    
    # STRETCH: Uncomment to run interactive menu
    main()
