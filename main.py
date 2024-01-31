import tkinter as tk
import ttkbootstrap as tb
from dotenv import dotenv_values
import requests
import time
import aiohttp
import asyncio

env_vars = dotenv_values('School Apps\Foodie\.env')
api_ninjas_api_key = env_vars.get("API_NINJAS_API_KEY")
wikimedia_api_key = env_vars.get("WIKI_MEDIA_API_KEY")

def getFoodDesc(search_query):
    language_code = 'en'
    number_of_results = 1
    headers = {
    'Authorization': "Bearer {}".format(wikimedia_api_key),
    'User-Agent': 'Foodie (bemdoo.maor1@gmail.com)'
    }

    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    parameters = {'q': search_query, 'limit': number_of_results}
    response = requests.get(url, headers=headers, params=parameters)
    return response.json().pages[0].excerpt
def show_loading_animation():
    loading_window = tb.Toplevel(root)
    loading_window.title("Loading")

    progress_bar = tb.Progressbar(loading_window, mode='indeterminate')
    progress_bar.pack(padx=10, pady=20)

    progress_bar.start()

    time.sleep(3)

    progress_bar.stop()

    loading_window.destroy()

def toHome():
    foods.forget()
    home.pack()


async def search():
    food = entry.get()
    api_url = 'https://api.api-ninjas.com/v1/recipe?query={}'.format(food)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url, headers={'X-Api-Key': api_ninjas_api_key}) as response:
                if response.status == 200:
                    res = await response.json()
                    if res:
                        for i, food in enumerate(res):
                            foodFrame = tb.Frame(foods, width=300, height=300, bootstyle="light")
                            foodTitle = tb.Label(foodFrame, text=food["title"], font=("Helvetica", 20), bootstyle="warning, inverse")
                            foodTitle.pack()
                            subFoodDescText = getFoodDesc(food["title"])
                            subFoodDesc = tb.Label(foodFrame, text=subFoodDescText, font=("Helvetica", 12), bootstyle="warning")
                            subFoodDesc.pack()
                            button = tb.Button(foodFrame, text="To Home", bootstyle="success", command=toHome)
                            button.pack(pady=10)
                            foodFrame.grid(padx=10, pady=10, row=i//3, column=i%3, sticky="nsew")
                        home.forget()
                        foods.pack()
                    else:
                        errorLabel.config(text="No results found")
                else:
                    print("Error:", response.status)
                    errorLabel.config(text="Error getting your foods. Please try again")
        except Exception as e:
            print("Exception:", e)
            errorLabel.config(text="An error occurred while searching. Please try again.")

root = tb.Window(title="Foodie", themename="darkly", iconphoto="School Apps/Foodie/assets/FOODIE.png")
# root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))
root.geometry("600x800")
root.place_window_center()

home = tb.Frame(root)
foods = tb.Frame(root)

# home page
home.pack()
image = tb.PhotoImage(file="School Apps/Foodie/assets/FOODIE.png")
label = tb.Label(home, image=image)
label.pack()

label2 = tb.Label(home, text="What would you like to prepare today?", justify="center", font=(
    "Helvetica", 20), wraplength=400, bootstyle="light")
label2.pack(pady=20)

entry = tb.Entry(home, width=50, bootstyle="warning")
entry.pack()

errorLabel = tb.Label(home, bootstyle="danger")
errorLabel.pack()

button = tb.Button(home, text="Search", bootstyle="warning", command=lambda: asyncio.run(search()))
button.pack(pady=20)

# foods page
# foodFrame = tb.Frame(foods, width=300, height=300)
# foodTitle = tb.Label(foodFrame, font=(
#     "Helvetica", 36), bootstyle="warning")
# foodTitle.pack()

# button = tb.Button(foodFrame, text="To Home", bootstyle="success", command=toHome)
# button.pack(pady=10)

root.after(1000, show_loading_animation)

root.mainloop()
