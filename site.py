import streamlit as st
import pandas as pd
import numpy as np

st.title('dados')
import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)

#2
import streamlit as st

code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code, language='python')

#3 

import streamlit as st
number = st.slider("Pick a number: ", min_value=1, max_value=10)
st.text("Your number is " + str(number))

#4
def load_data(url):
    df = pd.read_csv(url)  # 👈 Download the data
    return df

df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
st.dataframe(df)

st.button("Rerun")

#5

def transform(df):
    df = df.filter(items=['one', 'three'])
    df = df.apply(np.sum, axis=0)
    return df
#6

def add(arr1, arr2):
    return arr1 + arr2
#7
model = ("sentiment-analysis")  # 👈 Load the model

#8


@st.cache_data(ttl=3600)  # 👈 Cache data for 1 hour (=3600 seconds)
def get_api_data():
    data = api.get(...)
    return data
#9

@st.cache_data(max_entries=1000)  # 👈 Maximum 1000 entries in the cache
def get_large_array(seed):
    np.random.seed(seed)
    arr = np.random.rand(100000)
    return arr
#10
@st.cache_data(show_spinner=False)  # 👈 Disable the spinner
def get_api_data():
    data = api.get(...)
    return data

@st.cache_data(show_spinner="Fetching data from API...")  # 👈 Use custom text for spinner
def get_api_data():
    data = api.get(...)
    return data
#11
import streamlit as st

class MyCustomClass:
    def __init__(self, initial_score: int):
        self.my_score = initial_score

@st.cache_data
def multiply_score(obj: MyCustomClass, multiplier: int) -> int:
    return obj.my_score * multiplier

initial_score = st.number_input("Enter initial score", value=15)

score = MyCustomClass(initial_score)
multiplier = 2

st.write(multiply_score(score, multiplier))
#12
import streamlit as st

class MyCustomClass:
    def __init__(self, initial_score: int):
        self.my_score = initial_score

def hash_func(obj: MyCustomClass) -> int:
    return obj.my_score  # or any other value that uniquely identifies the object

@st.cache_data(hash_funcs={MyCustomClass: hash_func})
def multiply_score(obj: MyCustomClass, multiplier: int) -> int:
    return obj.my_score * multiplier

initial_score = st.number_input("Enter initial score", value=15)

score = MyCustomClass(initial_score)
multiplier = 2

st.write(multiply_score(score, multiplier))
#13
import streamlit as st

class MyCustomClass:
    def __init__(self, initial_score: int):
        self.my_score = initial_score

    @st.cache_data
    def multiply_score(self, multiplier: int) -> int:
        return self.my_score * multiplier

initial_score = st.number_input("Enter initial score", value=15)

score = MyCustomClass(initial_score)
multiplier = 2

st.write(score.multiply_score(multiplier))
#14
import streamlit as st

class MyCustomClass:
    def __init__(self, initial_score: int):
        self.my_score = initial_score

    @st.cache_data(hash_funcs={"__main__.MyCustomClass": lambda x: hash(x.my_score)})
    def multiply_score(self, multiplier: int) -> int:
        return self.my_score * multiplier

initial_score = st.number_input("Enter initial score", value=15)

score = MyCustomClass(initial_score)
multiplier = 2

st.write(score.multiply_score(multiplier))
#15
import streamlit as st

class MyCustomClass:
    def __init__(self, initial_score: int):
        self.my_score = initial_score

    @st.cache_data(hash_funcs={"__main__.MyCustomClass": id})
    def multiply_score(self, multiplier: int) -> int:
        return self.my_score * multiplier

initial_score = st.number_input("Enter initial score", value=15)

score = MyCustomClass(initial_score)
multiplier = 2

st.write(score.multiply_score(multiplier))
#16
import streamlit as st
from pydantic import BaseModel

class Person(BaseModel):
    name: str

@st.cache_data
def identity(person: Person):
    return person

person = identity(Person(name="Lee"))
st.write(f"The person is {person.name}")
#17
import streamlit as st
from pydantic import BaseModel

class Person(BaseModel):
    name: str

@st.cache_data(hash_funcs={Person: lambda p: p.name})
def identity(person: Person):
    return person

person = identity(Person(name="Lee"))
st.write(f"The person is {person.name}")
#18
import time
import numpy as np
import pandas as pd
import streamlit as st

@st.cache_data
def get_data():
    df = pd.DataFrame({"num": [112, 112, 2, 3], "str": ["be", "a", "be", "c"]})
    return df

@st.cache_data(hash_funcs={np.ndarray: str})
def show_data(data):
    time.sleep(2)  # This makes the function take 2s to run
    return data

df = get_data()
data = df["str"].unique()

st.dataframe(show_data(data))
st.button("Re-run")
#19
import time
import numpy as np
import pandas as pd
import streamlit as st

@st.cache_data
def get_data():
    df = pd.DataFrame({"num": [112, 112, 2, 3], "str": ["be", "a", "be", "c"]})
    return df

@st.cache_data
def show_data(data):
    time.sleep(2)  # This makes the function take 2s to run
    return data

df = get_data()
data = df["str"].unique()

st.dataframe(show_data(data))
st.button("Re-run")

#20
@st.cache_data
def get_api_data():
    data = api.get(...)
    st.success("Fetched data from API!")  # 👈 Show a success message
    return data
