import os
import avro.schema
import avro.io
import io

class ResearchDataManager:
    def __init__(self):
        self.entries = []
        self.filename = "research_data.avro"
        self.schema_file = "research_data_schema.avsc"
        self.schema = avro.schema.Parse(open(self.schema_file, "r").read())

    def add_entry(self, experiment_name, date, researcher, data_points):
        entry = {"experiment_name": experiment_name, "date": date, "researcher": researcher, "data_points": data_points}
        self.entries.append(entry)
    
    def get_entries(self):
        return self.entries
    
    def update_entry(self, index, experiment_name=None, date=None, researcher=None, data_points=None):
        if 0 <= index < len(self.entries):
            if experiment_name: self.entries[index]["experiment_name"] = experiment_name
            if date: self.entries[index]["date"] = date
            if researcher: self.entries[index]["researcher"] = researcher
            if data_points: self.entries[index]["data_points"] = data_points
    
    def delete_entry(self, index):
        if 0 <= index < len(self.entries):
            del self.entries[index]

    def save_entries_to_file(self):
        with open(self.filename, 'wb') as file:
            writer = avro.io.DatumWriter(self.schema)
            for entry in self.entries:
                bytes_writer = io.BytesIO()
                encoder = avro.io.BinaryEncoder(bytes_writer)
                writer.write(entry, encoder)
                file.write(bytes_writer.getvalue())
        print("Entries saved successfully.")
    
    def load_entries_from_file(self):
        if os.path.exists(self.filename):
            if os.path.getsize(self.filename) == 0:
                print("The file is empty. No data to load.")
                return
            with open(self.filename, 'rb') as file:
                reader = avro.io.DatumReader(self.schema)
                while True:
                    try:
                        # Ensure we are reading chunks of data correctly
                        bytes_reader = io.BytesIO(file.read())
                        decoder = avro.io.BinaryDecoder(bytes_reader)
                        if bytes_reader.getbuffer().nbytes == 0:
                            break  # End of file reached or no more data to read
                        entry = reader.read(decoder)
                        self.entries.append(entry)
                    except EOFError:
                        break  # End of file reached
                    except AssertionError as e:
                        print(f"Error reading entry: {e}")
                        break
                    except Exception as e:
                        print(f"Unexpected error: {e}")
                        break
        else:
            print("File not found.")

    def display_loaded_entries(self):
        if not self.entries:
            print("No entries loaded.")
        else:
            for index, entry in enumerate(self.entries, start=1):
                print(f"{index}: Experiment Name: {entry['experiment_name']}, Date: {entry['date']}, Researcher: {entry['researcher']}, Data Points: {entry['data_points']}")

    def analyze_data(self):
        for entry in self.entries:
            data_points = entry["data_points"]
            average = sum(data_points) / len(data_points)
            print(f"{entry['experiment_name']} (by {entry['researcher']} on {entry['date']}): Average = {average}")

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
        print("7. Load entries from Avro file")
        print("8. Display loaded entries")
        print("9. Exit")
        
        choice = input("Enter your choice: ")
        if choice == '1':
            experiment_name = input("Enter experiment name: ")
            date = input("Enter date (YYYY-MM-DD): ")
            researcher = input("Enter researcher's name: ")
            data_points = list(map(float, input("Enter data points separated by commas: ").split(',')))
            manager.add_entry(experiment_name, date, researcher, data_points)
        elif choice == '2':
            manager.display_loaded_entries()
        elif choice == '3':
            manager.display_loaded_entries()
            index = int(input("Enter the number of the entry you want to update: ")) - 1
            experiment_name = input("Enter new experiment name (leave blank to keep current): ")
            date = input("Enter new date (leave blank to keep current): ")
            researcher = input("Enter new researcher's name (leave blank to keep current): ")
            data_points = input("Enter new data points separated by commas (leave blank to keep current): ")
            data_points = list(map(float, data_points.split(','))) if data_points else None
            manager.update_entry(index, experiment_name, date, researcher, data_points)
        elif choice == '4':
            manager.display_loaded_entries()
            index = int(input("Enter the number of the entry you want to delete: ")) - 1
            manager.delete_entry(index)
        elif choice == '5':
            manager.analyze_data()
        elif choice == '6':
            manager.save_entries_to_file()
        elif choice == '7':
            manager.load_entries_from_file()
        elif choice == '8':
            manager.display_loaded_entries()
        elif choice == '9':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
