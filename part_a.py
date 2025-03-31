import os

# Function to add a research data entry
def add_entry(entries):
    experiment_name = input("Enter experiment name: ")
    date = input("Enter date (YYYY-MM-DD): ")
    researcher = input("Enter researcher's name: ")
    data_points = list(map(float, input("Enter data points separated by commas: ").split(',')))
    entry = [experiment_name, date, researcher] + data_points
    entries.append(entry)

# Function to view all research data entries
def view_entries(entries):
    for index, entry in enumerate(entries, start=1):
        print(f"{index}: {entry}")

# Function to update a research data entry
def update_entry(entries):
    view_entries(entries)
    index = int(input("Enter the number of the entry you want to update: ")) - 1
    if 0 <= index < len(entries):
        print("Leave blank if you don't want to change a field.")
        experiment_name = input(f"Enter new experiment name ({entries[index][0]}): ") or entries[index][0]
        date = input(f"Enter new date ({entries[index][1]}): ") or entries[index][1]
        researcher = input(f"Enter new researcher's name ({entries[index][2]}): ") or entries[index][2]
        data_points = input(f"Enter new data points separated by commas ({','.join(map(str, entries[index][3:]))}): ")
        data_points = list(map(float, data_points.split(','))) if data_points else entries[index][3:]
        entries[index] = [experiment_name, date, researcher] + data_points
        print("Entry updated successfully.")
    else:
        print("Invalid entry number.")

# Function to delete a research data entry
def delete_entry(entries):
    view_entries(entries)
    index = int(input("Enter the number of the entry you want to delete: ")) - 1
    if 0 <= index < len(entries):
        del entries[index]
        print("Entry deleted successfully.")
    else:
        print("Invalid entry number.")

# Function to save entries to a text file
def save_entries_to_file(entries, filename):
    with open(filename, 'w') as file:
        for entry in entries:
            file.write(','.join(map(str, entry)) + '\n')
    print("Entries saved successfully.")

# Function to load entries from a text file
def load_entries_from_file(filename):
    entries = []
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                entries.append(line.strip().split(','))
    else:
        print("File not found.")
    return entries

# Function to perform data analysis
def analyze_data(entries):
    for entry in entries:
        data_points = list(map(float, entry[3:]))
        average = sum(data_points) / len(data_points)
        print(f"{entry[0]} (by {entry[2]} on {entry[1]}): Average = {average}")

# Main function to interact with the user
def main():
    entries = []
    filename = "research_data.txt"
    
    while True:
        print("\nMenu:")
        print("1. Add a research data entry")
        print("2. View all entries")
        print("3. Update an entry")
        print("4. Delete an entry")
        print("5. Analyze data")
        print("6. Save entries to file")
        print("7. Load entries from file")
        print("8. Exit")
        
        choice = input("Enter your choice: ")
        if choice == '1':
            add_entry(entries)
        elif choice == '2':
            view_entries(entries)
        elif choice == '3':
            update_entry(entries)
        elif choice == '4':
            delete_entry(entries)
        elif choice == '5':
            analyze_data(entries)
        elif choice == '6':
            save_entries_to_file(entries, filename)
        elif choice == '7':
            entries = load_entries_from_file(filename)
        elif choice == '8':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
