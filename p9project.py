from ttkbootstrap import *
from ttkbootstrap.constants import *
from tkinter.messagebox import *
import sqlite3
import requests
from datetime import datetime
from PIL import Image, ImageTk 
from ttkbootstrap import Style



########## ========== Database Setup ===================================================================########
conn = sqlite3.connect("lovebirds_cafe.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    order_type TEXT NOT NULL,
    items TEXT
)
""")
conn.commit()


# ========== Fetch Location and Temperature =====================================================================

def get_location_and_temperature():
    try:
        response = requests.get("https://ipinfo.io/")
        data = response.json()
        city = data.get('city', 'Unknown')

        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=64726d6fb1fbe49d6430ac0eb7108ac2&units=metric"
        response = requests.get(weather_url)
        data = response.json()
        temp = data["main"]["temp"]

        return city, temp
    except Exception as e:
        return "Unknown", "N/A"

# ========== Main Window ================================================
app = Window(themename="flatly")
app.title("Lovebirds Cafe Order System")
app.geometry("700x700")


#=========================style and background=================================

style = Style()
style.configure("Transparent.TLabel", background="#d9d4ce")  # Match image background



# ====== Load and Set Background Image ======
bg_image_raw = Image.open("bird.jpg")  # Your image path
bg_image_raw = bg_image_raw.resize((700, 700), Image.Resampling.LANCZOS)
bg_image = ImageTk.PhotoImage(bg_image_raw)

# Create background label and place it behind all widgets
bg_label = Label(app, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


#======font created for large and smaall==========================================================
font_large = ("Arial", 18, "bold")
font_small = ("Arial", 12,"bold")

#============ Display location and temperature========================================================
city, temp = get_location_and_temperature()
location_label = Label(app, text=f"Location: {city} | Temperature: {temp}°C", font=font_small)
location_label.pack(pady=5)

# ========== Functions ============================================
def open_add():
    main_frame.pack_forget()
    add_frame.pack(fill=BOTH, expand=YES)

def open_view():
    main_frame.pack_forget()
    populate_view_orders()
    view_frame.pack(fill=BOTH, expand=YES)

def open_update():
    main_frame.pack_forget()
    update_frame.pack(fill=BOTH, expand=YES)

def open_delete():
    main_frame.pack_forget()
    delete_frame.pack(fill=BOTH, expand=YES)

def go_home(from_frame):
    from_frame.pack_forget()
    main_frame.pack(fill=BOTH, expand=YES)

def item_checkboxes(parent):
    items = []
    for text in ["Cold Coffee 🧋", "Ice Cream🍧", "Sandwich🥪", "Pizza🍕", "Burger🍔", "Fries🍟","Coco-Cola🍹","Pepsi🥤","Red-Bull🐂","Espresso☕︎","Cappuccino☕","Latte🍵","Mocha🧉","Americano☕","Hot Chocolate🍫"]:
        var = BooleanVar()
        chk = ttk.Checkbutton(parent, text=text, variable=var, bootstyle="success-round-toggle")
        chk.var = var
        chk.pack(anchor="w", padx=20)
        items.append(chk)
    return items

# ========== Add Order ================================================================================


def add_order_to_db():
    oid = add_id.get()
    name = add_name.get()
    phone = add_phone.get()
    otype = order_type.get()

    selected_items = [chk.cget("text") for chk in add_items if chk.var.get()]
    items_str = ",".join(selected_items)

    if oid and name and phone:
        try:
            cursor.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", (oid, name, phone, otype, items_str))
            conn.commit()
            showinfo("Success", "Order added successfully!")
            add_id.delete(0, END)
            add_name.delete(0, END)
            add_phone.delete(0, END)
            order_type.set("DineIn")
            for chk in add_items:
                chk.var.set(False)
        except sqlite3.IntegrityError:
            showerror("Error", "Order ID already exists.")
    else:
        showerror("Input Error", "Please fill all fields.")



# ========== View Orders ===================================================================



def populate_view_orders():
    for row in view_tree.get_children():
        view_tree.delete(row)
    cursor.execute("SELECT * FROM orders")
    for row in cursor.fetchall():
        view_tree.insert("", END, values=row)

# ========== Update Order ========================================================================

def update_order():
    oid = update_id.get()
    name = update_name.get()
    phone = update_phone.get()
    otype = update_order_type.get()

    selected_items = [chk.cget("text") for chk in update_items if chk.var.get()]
    items_str = ",".join(selected_items)

    if oid and name and phone:
        cursor.execute("SELECT * FROM orders WHERE order_id = ?", (oid,))
        if cursor.fetchone():
            cursor.execute("UPDATE orders SET name = ?, phone = ?, order_type = ?, items = ? WHERE order_id = ?",
                           (name, phone, otype, items_str, oid))
            conn.commit()
            showinfo("Success", "Order updated successfully!")
        else:
            showerror("Error", "Order ID does not exist.")
    else:
        showerror("Input Error", "Please fill all fields.")

# ========== Delete Order ===================================================================


def delete_order():
    oid = delete_id.get()
    if not oid:
        showerror("Input Error", "Please enter an Order ID.")
        return
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (oid,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM orders WHERE order_id = ?", (oid,))
        conn.commit()
        showinfo("Deleted", "Order deleted successfully.")
        delete_id.delete(0, END)
    else:
        showerror("Error", "Order ID not found.")

# ========== Main Menu ==========

main_frame = Frame(app,bootstyle=INFO)
main_frame.pack(fill=BOTH, expand=YES)

# ====== Load and Set Background Image ======

bg_image_raw = Image.open("bird.jpg") 
bg_image_raw = bg_image_raw.resize((1900, 1000), Image.Resampling.LANCZOS)
bg_image = ImageTk.PhotoImage(bg_image_raw)

# Create background label and place it behind all widgets
bg_label = Label(main_frame, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


Label(main_frame, text="💕💕 ʟᴏᴠᴇ  ʙɪʀᴅꜱ ᴄᴀꜰᴇ 💕💕",style="Transparent.TLabel",bootstyle=SUCCESS, font=font_large).pack(pady=30)

Button(main_frame, text="Add Order", style="Custom.TButton",     width=50,   bootstyle=PRIMARY,  command=open_add).pack(pady=10)
Button(main_frame, text="View Order",    width=50,   bootstyle=SUCCESS,  command=open_view).pack(pady=10)
Button(main_frame, text="Update Order",  width=50,   bootstyle=WARNING,  command=open_update).pack(pady=10)
Button(main_frame, text="Delete Order",  width=50,   bootstyle=DANGER,   command=open_delete).pack(pady=10)

# ========== Add Frame ==========
add_frame = Frame(app)

Label(add_frame, text="💕💕Add Order💕💕", font=font_large).pack(pady=20)

Label(add_frame, text="Order ID",  font=font_small).pack()
add_id = Entry(add_frame, font=font_small)
add_id.pack(pady=5, fill=X, padx=30)

Label(add_frame, text="Name",font=font_small).pack()
add_name = Entry(add_frame, font=font_small)
add_name.pack(pady=5, fill=X, padx=30)

Label(add_frame, text="Phone", font=font_small).pack()
add_phone = Entry(add_frame, font=font_small)
add_phone.pack(pady=5, fill=X, padx=30)

Label(add_frame, text="Order Type", font=font_small).pack(pady=10)
order_type = StringVar(value="DineIn")
Radiobutton(add_frame, text="DineIn", variable=order_type, value="DineIn").pack()
Radiobutton(add_frame, text="TakeAway",variable=order_type, value="TakeAway").pack()

Label(add_frame, text="Items", font=font_small).pack(pady=10)
add_items = item_checkboxes(add_frame)

Button(add_frame, text="Submit Order", bootstyle=SUCCESS, command=add_order_to_db).pack(pady=10)
Button(add_frame, text="Back", bootstyle=SECONDARY, command=lambda: go_home(add_frame)).pack(pady=10)

# ========== View Frame ==========
view_frame = Frame(app)


#background image for view frame
view_bg_raw = Image.open("4784311.jpg")  # or another image
view_bg_raw = view_bg_raw.resize((1900, 1000), Image.Resampling.LANCZOS)
view_bg_image = ImageTk.PhotoImage(view_bg_raw)

view_bg_label = Label(view_frame, image=view_bg_image)
view_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
Label(view_frame, text="💕💕View Orders💕💕",style="Transparent.TLabel", font=font_large).pack(pady=20)

columns = ("Order ID", "Name", "Phone NO", "Order Type", "Items")
view_tree = Treeview(view_frame, columns=columns, show="headings")
for col in columns:
    view_tree.heading(col, text=col)
    view_tree.column(col, width=20)
view_tree.pack(pady=1, fill=BOTH, padx= 60)

Button(view_frame, text="Back",bootstyle=DANGER, command=lambda: go_home(view_frame)).pack(pady=10)

# ========== Update Frame ==========
update_frame = Frame(app,)
Label(update_frame, text="💕💕Update Order💕💕", font=font_large).pack(pady=20)

Label(update_frame, text="Order ID", font=font_small).pack()
update_id = Entry(update_frame, font=font_small)
update_id.pack(pady=5, fill=X, padx=30)

Label(update_frame, text="Name", font=font_small).pack()
update_name = Entry(update_frame, font=font_small)
update_name.pack(pady=5, fill=X, padx=30)

Label(update_frame, text="Phone", font=font_small).pack()
update_phone = Entry(update_frame, font=font_small)
update_phone.pack(pady=5, fill=X, padx=30)

Label(update_frame, text="Order Type", font=font_small).pack(pady=10)
update_order_type = StringVar(value="DineIn")
Radiobutton(update_frame, text="DineIn", variable=update_order_type, value="DineIn").pack()
Radiobutton(update_frame, text="TakeAway", variable=update_order_type, value="TakeAway").pack()

Label(update_frame, text="Items", font=font_small).pack(pady=10)
update_items = item_checkboxes(update_frame)

Button(update_frame, text="Update Order", bootstyle=SUCCESS, command=update_order).pack(pady=10)
Button(update_frame, text="Back", bootstyle=SECONDARY, command=lambda: go_home(update_frame)).pack(pady=10)

# ========== Delete Frame ==========
delete_frame = Frame(app)

# ---------Background for delete frame ----------

delete_bg_raw = Image.open("lovee.jpg")  # or another image
delete_bg_raw = delete_bg_raw.resize((1900, 1000), Image.Resampling.LANCZOS)
delete_bg_image = ImageTk.PhotoImage(delete_bg_raw)
delete_bg_label = Label(delete_frame, image=delete_bg_image)
delete_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

Label(delete_frame, text="💕💕Delete Order💕💕",style="Transparent.TLabel", font=font_large).pack(pady=20)

# Create a frame to hold Order ID label and entry (grid used inside this frame)
id_row = ttk.Frame(delete_frame)
id_row.pack(pady=10)

Label(id_row, text=" Order ID : ", font=font_small).grid(row=0, column=0, padx=5, sticky="e")
Label(id_row, text=" Order ID : ", font=font_small).grid(row=0, column=0, padx=5, sticky="e")

delete_id = Entry(id_row, font=font_small)
delete_id.grid(row=0, column=1, padx=5)





Button(delete_frame, text="Delete", bootstyle="danger", command=delete_order).pack(pady=10)
Button(delete_frame, text="Back", bootstyle="secondary", command=lambda:go_home(delete_frame)).pack(pady=10)
# ========== Start App #========= End Game =========== #

app.mainloop()
