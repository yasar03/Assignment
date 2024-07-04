import tkinter as tk
from tkinter import ttk, messagebox
import requests

def query_game_data():
    player = player_entry.get()
    try:
        response = requests.get(f'http://localhost:5000/?AppID={player}')
        response.raise_for_status()
        data = response.json()
        display_results(data)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")

def display_results(data):
    for row in tree.get_children():
        tree.delete(row)
    if data:
        for item in data:
            tree.insert('', 'end', values=(item['player'], item['score'], item['level'], item['timestamp']))
    else:
        messagebox.showinfo("Info", "No data found")

app = tk.Tk()
app.title("Game Data Query")

# Create and place the input field
tk.Label(app, text="Enter player name:").grid(row=0, column=0, padx=10, pady=10)
player_entry = tk.Entry(app)
player_entry.grid(row=0, column=1, padx=10, pady=10)

# Create and place the query button
query_button = tk.Button(app, text="Query", command=query_game_data)
query_button.grid(row=0, column=2, padx=10, pady=10)

# Create and place the Treeview widget for displaying results
tree = ttk.Treeview(app, columns=('Player', 'Score', 'Level', 'Timestamp'), show='headings')
tree.heading('Player', text='Player')
tree.heading('Score', text='Score')
tree.heading('Level', text='Level')
tree.heading('Timestamp', text='Timestamp')
tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

app.mainloop()
