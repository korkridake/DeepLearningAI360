#!/usr/bin/env python
# coding: utf-8

# # L3: Retry-based Structured Output

# <p style="background-color:#fff6e4; padding:15px; border-width:3px; border-color:#f5ecda; border-style:solid; border-radius:6px"> ⏳ <b>Note <code>(Kernel Starting)</code>:</b> This notebook takes about 30 seconds to be ready to use. You may start and watch the video while you wait.</p>

# In[1]:


import os
from utils import get_together_api_key


# In[2]:


import instructor
from openai import OpenAI

# Instantiate the client
together_client = OpenAI(
    base_url=f"{os.getenv('DLAI_TOGETHER_API_BASE', 'https://api.together.xyz')}/v1",
    api_key=get_together_api_key()
)


# <div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">
# <p> 💻 &nbsp; <b>Access <code>requirements.txt</code> and <code>helper.py</code> files:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Open"</em>.
# 
# <p> ⬇ &nbsp; <b>Download Notebooks:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Download as"</em> and select <em>"Notebook (.ipynb)"</em>.</p>
# 
# <p> 📒 &nbsp; For more help, please see the <em>"Appendix – Tips, Help, and Download"</em> Lesson.</p>
# </div>

# In[3]:


response = together_client.chat.completions.create(
    model='meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo',
    messages = [{
        "role": "user", 
        "content": 'sup'
    }]
)

response.choices[0].message.content


# ## Adding Instructor

# In[4]:


# Wrap together with the instructor client
instructor_client = instructor.from_openai(together_client)


# In[5]:


from pydantic import BaseModel

class Greeting(BaseModel):
    hello: str


# In[6]:


response = instructor_client.chat.completions.create(
    model='meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo',
    messages = [{
        "role": "user", 
        "content": 'sup'
    }], 
    # Note: OpenAI uses response_format, instructor
    #       uses response_model!
    response_model=Greeting
)

response


# ## Defining a calendar event

# In[7]:


from pydantic import Field
from datetime import date
from typing import List

# Person only has a name, but we can easily extend it with other fields
class Person(BaseModel):
    name: str

class CalendarEvent(BaseModel):
    name: str
    
    # not supported by OpenAI. We want a format like 2025-01-30
    date: date 
    participants: List[Person]

    address_number: str
    street_name: str
    city_name: str

    # Inline regex patterns not supported by OpenAI restrict state code 
    # to be two capital letters (OpenAI does not support pattern fields)
    state_code: str = Field(pattern=r'[A-Z]{2}')

    # Zip code must be five digits
    zip_code: str = Field(pattern=r'\d{5}') 


# In[8]:


event_description = """
Alice and Bob are going to a science fair on Friday, January 2024.
The science fair is hosted at the gymnasium of Hazeldale Elementary
School at 20080 SW Farmington Road in Beaverton Oregon.
"""


# In[9]:


def generate(
    response_model, 
    user_prompt, 
    system_prompt="You are a helpful assistant.",
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    # Can use 70b for a higher-quality model
    # model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    max_retries=3,
):
    event = instructor_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt
            },
        ],
        response_model=response_model,
        max_retries=max_retries
    )

    return event


# In[10]:


system_prompt = """
Make a calendar event. Respond in JSON with
the event name, date, list of participants,
and the address.
"""

user_prompt = 'Event description: ' + event_description

event = generate(
    CalendarEvent, 
    user_prompt, 
    system_prompt=system_prompt
)


# In[11]:


event


# ## Retries

# In[12]:


from utils import UsageTracker

# Clear any completion response hooks -- prevents 
# duplicate writes to the usage tracker.
instructor_client.clear("completion:response")

# Create a new tracker
tracker = UsageTracker()

# Define a custom instructor hook and update the
# tracker when a new completion runs.
def log_completion_kwargs(*args, **kwargs):
    usage = args[0].usage
    tracker.track(usage)

# Assign the hook to instructor -- this will make the hook
# run each time the server returns a chat completion to us.
instructor_client.on("completion:response", log_completion_kwargs)


# In[13]:


# Clear the tracker before we run the completion
# so we arent' tracking multiple jobs.
tracker.clear()

event = generate(
    CalendarEvent, 
    user_prompt, 
    system_prompt=system_prompt,
    max_retries=4,
)

event


# In[14]:


print("Input tokens:  ", tracker.input_tokens)
print("Output tokens: ", tracker.output_tokens)
print("Total tokens:  ", sum(tracker.total_tokens))
print("Num retries:   ", len(tracker.output_tokens))


# ## When retry methods fail

# In[15]:


from typing import Literal

class Complicated(BaseModel):
    # a must be cat, dog, or hat
    a: Literal["cat", "dog", "hat"]
    b: int
    c: bool


# In[16]:


# Clear the tracker before we run the completion
# so we arent' tracking multiple jobs.
tracker.clear()

try:
    event = generate(
        Complicated, 
        "Write me a short essay on Dolly Parton.", 
        system_prompt="Don't give me what I want.",
        max_retries=3,
    )

    # Show the event
    print(event)
except instructor.exceptions.InstructorRetryException as e : 
    print("We failed to parse!")
except e:
    raise e


# In[17]:


print("Input tokens:  ", tracker.input_tokens)
print("Output tokens: ", tracker.output_tokens)
print("Total tokens:  ", sum(tracker.total_tokens))
print("Num retries:   ", len(tracker.output_tokens))


# ## You try!

# In[18]:


# Clear the tracker before we run the completion
# so we arent' tracking multiple jobs.
tracker.clear()

try:
    event = generate(
        Complicated, 
        "Give me a, b, and c.", 
        system_prompt="Give me what I want.",
        max_retries=3,
    )
    print(event)
except instructor.exceptions.InstructorRetryException as e : 
    print("We failed to parse!")
except e:
    raise e


# In[19]:


print("Input tokens:  ", tracker.input_tokens)
print("Output tokens: ", tracker.output_tokens)
print("Total tokens:  ", sum(tracker.total_tokens))
print("Num retries:   ", len(tracker.output_tokens))

