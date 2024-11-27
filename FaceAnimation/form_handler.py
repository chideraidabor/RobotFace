from tkinter import Tk, Label, Entry, Button, StringVar, Radiobutton

def show_form():
    def submit_form():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        purpose = var_purpose.get()
        other_details = other_entry.get()

        # Print form details
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Purpose: {purpose}")
        print(f"Other Details: {other_details}")

        root.destroy()

    root = Tk()
    root.title("Appointment Form")
    root.geometry("400x300")
    root.configure(bg="light blue")

    Label(root, text="First Name:", bg="light blue").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    first_name_entry = Entry(root, width=30)
    first_name_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(root, text="Last Name:", bg="light blue").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    last_name_entry = Entry(root, width=30)
    last_name_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(root, text="Purpose:", bg="light blue").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    var_purpose = StringVar(value="Appointment")
    Radiobutton(root, text="Appointment", variable=var_purpose, value="Appointment", bg="light blue").grid(row=2, column=1, sticky="w")
    Radiobutton(root, text="Other", variable=var_purpose, value="Other", bg="light blue").grid(row=3, column=1, sticky="w")

    Label(root, text="If Other, specify:", bg="light blue").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    other_entry = Entry(root, width=30)
    other_entry.grid(row=4, column=1, padx=10, pady=5)

    Button(root, text="Submit", command=submit_form, bg="green", fg="white").grid(row=5, column=0, columnspan=2, pady=20)

    root.mainloop()

if __name__ == "__main__":
    show_form()
