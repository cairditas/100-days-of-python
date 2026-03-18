import tkinter as tk


def clicked(input):
    result = float(input.get()) * 1.609
    conversion.config(text=f"{result:.2f}")

window = tk.Tk()
window.title("Miles to Km converter")
window.minsize(width=500, height=300)
window.config(padx=100, pady=100)

input = tk.Entry(width=10);
input.grid(row=0, column=1);

miles = tk.Label(text="Miles")
miles.grid(row=0, column=2)

equal = tk.Label(text="is equal to")
equal.grid(row=1, column=0)

conversion = tk.Label(text="0", width=10);
conversion.grid(row=1, column=1);

km = tk.Label(text="KM")
km.grid(row=1, column=2)

button = tk.Button(text="Convert", command=lambda: clicked(input))
button.grid(row=2, column=1)  

window.mainloop()