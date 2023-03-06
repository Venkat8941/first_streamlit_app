import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError 
streamlit.title("My Mom's New Healthy Diner") 
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oameal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast') streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇') #import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit') 
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected =streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected] # Display the table on the page. streamlit.dataframe(fruits_to_show) #create the repeatable code block(called function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return (fruityvice_normalized) streamlit.header("Fruityvice Fruit Advice!")
#Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function=get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error() #don't run anything past here while we troubleshoot
streamlit.stop() #import snowflake.connector 
streamlit.header("The fruit load list contains :")
#Snowflake-related funtions
def get_fruit_load_list():
  with my_cnx as cursor():
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
#Add a button to load the fruit
if streamlit.button('Get Fruir Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows =get_fruit_load_list()
  streamlit.dataframe(my_data_rows) 
#Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit) #This will not work correctly, but jsut go with it for now
my_cur.execute("insert into fruit_load_list values('from streamlit')")
