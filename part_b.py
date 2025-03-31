import os

class ResearchDataManager:
    def __init__(self):
        self.entries = []
        self.filename = "research_data.txt"
    
    def add_entry(self):
        experiment_name = input("Enter experiment name: ")
        date = input("Enter date (YYYY-MM-DD): ")
        researcher = input("Enter researcher's name: ")
        data_points = list(map(float, input("Enter data points separated by commas: ").split(',')))
        entry = [experiment_name, date, researcher] + data_points
        self.entries.append(entry)
    
    def view_entries(self):
        for index, entry in enumerate(self.entries, start=1):
            print(f"{index}: {entry}")
    
    def update_entry(self):
        self.view_entries()
        index = int(input("Enter the number of the entry you want to update: ")) - 1
        if 0 <= index < len(self.entries):
            print("Leave blank if you don't want to change a field.")
            experiment_name = input(f"Enter new experiment name ({self.entries[index][0]}): ") or self.entries[index][0]
            date = input(f"Enter new date ({self.entries[index][1]}): ") or self.entries[index][1]
            researcher = input(f"Enter new researcher's name ({self.entries[index][2]}): ") or self.entries[index][2]
            data_points = input(f"Enter new data points separated by commas ({','.join(map(str, self.entries[index][3:]))}): ")
            data_points = list(map(float, data_points.split(','))) if data_points else self.entries[index][3:]
            self.entries[index] = [experiment_name, date, researcher] + data_points
            print("Entry updated successfully.")
        else:
            print("Invalid entry number.")
    
    def delete_entry(self):
        self.view_entries()
        index = int(input("Enter the number of the entry you want to delete: ")) - 1
        if 0 <= index < len(self.entries):
            del self.entries[index]
            print("Entry deleted successfully.")
        else:
            print("Invalid entry number.")
    
    def save_entries_to_file(self):
        with open(self.filename, 'w') as file:
            for entry in self.entries:
                file.write(','.join(map(str, entry)) + '\n')
        print("Entries saved successfully.")
    
    def load_entries_from_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.entries = [line.strip().split(',') for line in file]
        else:
            print("File not found.")
    
    def analyze_data(self):
        for entry in self.entries:
            data_points = list(map(float, entry[3:]))
            average = sum(data_points) / len(data_points)
            print(f"{entry[0]} (by {entry[2]} on {entry[1]}): Average = {average}")

def main():
    manager = ResearchDataManager()
    
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
            manager.add_entry()
        elif choice == '2':
            manager.view_entries()
        elif choice == '3':
            manager.update_entry()
        elif choice == '4':
            manager.delete_entry()
        elif choice == '5':
            manager.analyze_data()
        elif choice == '6':
            manager.save_entries_to_file()
        elif choice == '7':
            manager.load_entries_from_file()
        elif choice == '8':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
