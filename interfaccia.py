
import streamlit as st
from datetime import datetime
from streamlit_option_menu import option_menu
import requests
from PIL import Image

iconUser = Image.open('userAvatar.jpeg')

logo = st.image("logo.jpeg", width=200) 

variables =[
  "X_Y_Z_A_C1_SPB1__Machine__Machine_State",
  "X_Y_Z_A_C1_SPB1__Machine__Machine_Stop_Condition",
  "X_Y_Z_A_C1_SPB1__PartProgram__Part_Program",
  "X_Y_Z_A_C1_SPB1__PartProgram__Part_Program_Info_Block",
  "X_Y_Z_A_C1_SPB1__PartProgram__Part_Program_Line_Number",
  "X_Y_Z_A_C1_SPB1__PartProgram__Part_Program_Working",
  "X_Y_Z_A_C1_SPB1__PartProgram__Part_Program_Working_Name",
  "X_Y_Z_A_C1_SPB1__PartProgram__Working_Program_Name",
  "X_Y_Z_A_C1_SPB1__PartProgram__Part_Program_Main_Job",
  "X_Y_Z_A_C1_SPB1__PartProgram__Part_Program_Name",
  "X_Y_Z_A_C1_SPB1__PartProgram__Part_Program_Status",
  "X_Y_Z_A_C1_SPB1__Machine__Work_Pieces_Count",
  "A__Axis__Actual_Feed_Rate_Override",
  "A__Axis__Actual_Feed_Rate",
  "A__Axis__Drive_Load",
  "A__Axis__Perc_Feed_Override",
  "A__Axis__Position",
  "A__Axis__Rotary_Speed",
  "A__Axis__Speed",
  "A__Axis__Travel_Distance",
  "A__Axis__Travel_Time",
  "A__Motor__Current",
  "A__Motor__Power",
  "A__Motor__Torque",
  "C1__Axis__Actual_Feed_Rate_Override",
  "C1__Axis__Actual_Feed_Rate",
  "C1__Axis__Drive_Load",
  "C1__Axis__Perc_Feed_Override",
  "C1__Axis__Position",
  "C1__Axis__Rotary_Speed",
  "C1__Axis__Speed",
  "C1__Axis__Travel_Distance",
  "C1__Axis__Travel_Time",
  "C1__Motor__Current",
  "C1__Motor__Power",
  "C1__Motor__Torque",
  "SPB1__Axis__Actual_Feed_Rate_Override",
  "SPB1__Axis__Actual_Feed_Rate",
  "SPB1__Axis__Drive_Load",
  "SPB1__Axis__Perc_Feed_Override",
  "SPB1__Axis__Position",
  "SPB1__Axis__Rotary_Speed",
  "SPB1__Axis__Speed",
  "SPB1__Axis__Travel_Distance",
  "SPB1__Axis__Travel_Time",
  "SPB1__Motor__Current",
  "SPB1__Motor__Power",
  "SPB1__Motor__Torque",
  "X__Axis__Actual_Feed_Rate_Override",
  "X__Axis__Actual_Feed_Rate",
  "X__Axis__Drive_Load",
  "X__Axis__Perc_Feed_Override",
  "X__Axis__Position",
  "X__Axis__Rotary_Speed",
  "X__Axis__Speed",
  "X__Axis__Travel_Distance",
  "X__Axis__Travel_Time",
  "X__Motor__Current",
  "X__Motor__Power",
  "X__Motor__Torque",
  "Y__Axis__Actual_Feed_Rate_Override",
  "Y__Axis__Actual_Feed_Rate",
  "Y__Axis__Drive_Load",
  "Y__Axis__Perc_Feed_Override",
  "Y__Axis__Position",
  "Y__Axis__Rotary_Speed",
  "Y__Axis__Speed",
  "Y__Axis__Travel_Distance",
  "Y__Axis__Travel_Time",
  "Y__Motor__Current",
  "Y__Motor__Power",
  "Y__Motor__Torque",
  "Z__Axis__Actual_Feed_Rate_Override",
  "Z__Axis__Actual_Feed_Rate",
  "Z__Axis__Drive_Load",
  "Z__Axis__Perc_Feed_Override",
  "Z__Axis__Position",
  "Z__Axis__Rotary_Speed",
  "Z__Axis__Speed",
  "Z__Axis__Travel_Distance",
  "Z__Axis__Travel_Time",
  "Z__Motor__Current",
  "Z__Motor__Power",
  "Z__Motor__Torque",
  "A__Motor__Temperature",
  "C1__Motor__Temperature",
  "SPB1__Motor__Temperature",
  "X__Motor__Temperature",
  "Y__Motor__Temperature",
  "Z__Motor__Temperature"
]


import requests
import streamlit as st
from datetime import datetime
import time

# Used for creating the body in the 'Rivet format'
def replace_keys(data):
    new_data = []
    for entry in data:
        new_entry = {
            'type': entry['role'],
            'message': entry['content']
        }
        new_data.append(new_entry)
    oggett = { "input": new_data}
    return oggett


# Function to get the bot response
def get_bot_response(prompt, msgs): 
    base_url = "http://localhost:3001/api/rivet-example"
    data = replace_keys(msgs)
    print(data)

    try:
        response = requests.post(base_url, json=data)
        response.raise_for_status()
        data = response.json()
        print('RISPOSTA: ', data)
        return data.get("output", "No response from the bot."), data.get("image", None)
    except requests.exceptions.RequestException as e:
        return f"Error: {e}", None


# Main function
def main():
    st.title("PlantMate")

    # Initialize session state variables
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""
    if "reset_text_area" not in st.session_state:
        st.session_state.reset_text_area = False
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar inputs
    startdata_selection = st.sidebar.date_input("Select start date", datetime.today())
    starthour_seletion = st.sidebar.time_input("Select start time")
    enddata_selection = st.sidebar.date_input("Select end date", datetime.today())
    endhour_seletion = st.sidebar.time_input("Select end time")
    plant_selection = st.sidebar.selectbox("Which Plant are you interested in?", ('','EVO', 'Plant 2'))

    # Workcenter and asset selection based on plant
    if plant_selection == "EVO":
        workcenter_selection = st.sidebar.selectbox("Which Workcenter are you interested in?", ['','521', 'Workcenter 2'], index=1)
        if workcenter_selection == '521':
            asset_selection = st.sidebar.selectbox("Which Asset are you interested in?", ['','82069'])
            if asset_selection == '82069':
                variable_selection = st.sidebar.multiselect("Which variable are you interested in?", variables)
        # elif workcenter_selection == 'Workcenter 2':
        #     asset_selection = st.sidebar.selectbox("Which Asset are you interested in?", ['','Asset 5', 'Asset 6', 'Asset 7', 'Asset 8'])
        #     if asset_selection in ['Asset 5', 'Asset 6', 'Asset 7', 'Asset 8']:
        #         variable_selection = st.sidebar.multiselect("Which variable are you interested in?", variables)
    # elif plant_selection == "Plant 2":
    #     workcenter_selection = st.sidebar.selectbox("Which Workcenter are you interested in?", ["","Workcenter 3", "Workcenter 4"], index=1)
    #     if workcenter_selection == 'Workcenter 3':
    #         asset_selection = st.sidebar.selectbox("Which Asset are you interested in?", ['','Asset 9', 'Asset 10', 'Asset 11', 'Asset 12'])
    #         if asset_selection in ['Asset 9', 'Asset 10', 'Asset 11', 'Asset 12']:
    #             variable_selection = st.sidebar.multiselect("Which variable are you interested in?", variables)
    #     elif workcenter_selection == 'Workcenter 4':
    #         asset_selection = st.sidebar.selectbox("Which variable are you interested in?", ['','Asset 13', 'Asset 14', 'Asset 15', 'Asset 16'])
    #         if asset_selection in ['Asset 13', 'Asset 14', 'Asset 15', 'Asset 16']:
    #             variable_selection = st.sidebar.multiselect("Which variable are you interested in?", variables)

    # Function to send chat data
    def send_to_chat():
        chat_input = ""
        chat_input += f"Plant {plant_selection}, workcenter {workcenter_selection}, asset {asset_selection}, "
        chat_input += f"Data di inizio: {startdata_selection} {starthour_seletion} "
        chat_input += f"Data di fine: {enddata_selection} {endhour_seletion} "
        chat_input += "Variabili selezionate:\n"
        for variabile in variable_selection:
            chat_input += variabile + "\n"

        st.session_state.messages.append({"role": "user", "content": chat_input})
        st.session_state.reset_text_area = True
        st.experimental_rerun()  # Force rerun to update the UI

    # Function to clear messages
    def clear_messages():
        st.session_state.messages = []
        st.experimental_rerun()  # Force rerun to update the UI

    # Display all chat messages in a container
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == 'assistant':
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    if "image" in message:
                        st.image(message["image"])
            else:
                with st.chat_message(message["role"], avatar=iconUser):
                    st.markdown(message["content"])

    # Chat input and clear button at the bottom
    col1, col2 = st.columns([4, 1])
    with col1:
        prompt = st.chat_input("How can I assist you?")
    with col2:
        if st.button('Clear Messages'):
            clear_messages()

    # Handle chat input and append messages
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Send the user input to a chatbot API and get the response
        response, image = get_bot_response(prompt, st.session_state.messages)
        
        assistant_message = {"role": "assistant", "content": response}
        if image:
            assistant_message["image"] = image
        st.session_state.messages.append(assistant_message)
        
        st.experimental_rerun()  # Force rerun to update the UI

    if st.button("Transfer variables"):
        send_to_chat()

if __name__ == "__main__":
    main()


