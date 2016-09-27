import csv


def save_csv(contacts=list(), file="phone_book.csv"):
    if type(contacts) is list:
        with open(file, "w", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(["first_name", "last_name", "phone_number"])
            for k in contacts:
                writer.writerow([k.first_name, k.last_name, k.phone_number])
        return "Phone Book data was successfully saved to .csv file."
    else:
        return "Phone Book is empty."
