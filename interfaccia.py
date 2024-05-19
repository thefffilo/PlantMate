
import streamlit as st
from datetime import datetime
from streamlit_option_menu import option_menu
import requests
from PIL import Image

iconUser = Image.open('userAvatar.jpeg')

logo = st.image("logo.jpeg", width=200) 

variables = ["X_Y_Z_A_C1_SPB1_Machine_Machine_State",
 "X_Y_Z_A_C1_SPB1_Machine_Machine_Stop_Condition",
 "X_Y_Z_A_C1_SPB1_PartProgram_Part_Program",
 "X_Y_Z_A_C1_SPB1_PartProgram_Part_Program_Info_Block",
 "X_Y_Z_A_C1_SPB1_PartProgram_Part_Program_Line_Number",
 "X_Y_Z_A_C1_SPB1_PartProgram_Part_Program_Working",
 "X_Y_Z_A_C1_SPB1_PartProgram_Part_Program_Working_Name",
 "X_Y_Z_A_C1_SPB1_PartProgram_Working_Program_Name",
 "X_Y_Z_A_C1_SPB1_PartProgram_Part_Program_Main_Job",
 "X_Y_Z_A_C1_SPB1_PartProgram_Part_Program_Name",
 "X_Y_Z_A_C1_SPB1_PartProgram_Part_Program_Status",
 "X_Y_Z_A_C1_SPB1_Machine_Work_Pieces_Count",
 "A_Axis_Actual_Feed_Rate_Override",
 "A_Axis_Actual_Feed_Rate",
 "A_Axis_Drive_Load",
 "A_Axis_Perc_Feed_Override",
 "A_Axis_Position",
 "A_Axis_Rotary_Speed",
 "A_Axis_Speed",
 "A_Axis_Travel_Distance",
 "A_Axis_Travel_Time",
 "A_Motor_Current", "A_Motor_Power", "A_Motor_Torque",
 "C1_Axis_Actual_Feed_Rate_Override",
 "C1_Axis_Actual_Feed_Rate","C1_Axis_Drive_Load",
 "C1_Axis_Perc_Feed_Override",
 "C1_Axis_Position","C1_Axis_Rotary_Speed","C1_Axis_Speed",
 "C1_Axis_Travel_Distance",
 "C1_Axis_Travel_Time", "C1_Motor_Current", "C1_Motor_Power",
 "C1_Motor_Torque", "SPB1_Axis_Actual_Feed_Rate_Override",
 "SPB1_Axis_Actual_Feed_Rate",
 "SPB1_Axis_Drive_Load", "SPB1_Axis_Perc_Feed_Override", 
 "SPB1_Axis_Position", "SPB1_Axis_Rotary_Speed",
 "SPB1_Axis_Speed",  "SPB1_Axis_Travel_Distance",
 "SPB1_Axis_Travel_Time", "SPB1_Motor_Current",
 "SPB1_Motor_Power", "SPB1_Motor_Torque",
 "X_Axis_Actual_Feed_Rate_Override",
 "X_Axis_Actual_Feed_Rate", "X_Axis_Drive_Load",
 "X_Axis_Perc_Feed_Override", "X_Axis_Position",
 "X_Axis_Rotary_Speed", "X_Axis_Speed",
 "X_Axis_Travel_Distance", "X_Axis_Travel_Time",
 "X_Motor_Current", "X_Motor_Power", "X_Motor_Torque",
 "Y_Axis_Actual_Feed_Rate_Override", 
 "Y_Axis_Actual_Feed_Rate", "Y_Axis_Drive_Load",
 "Y_Axis_Perc_Feed_Override", "Y_Axis_Position",
 "Y_Axis_Rotary_Speed", "Y_Axis_Speed", "Y_Axis_Travel_Distance",
 "Y_Axis_Travel_Time", "Y_Motor_Current", "Y_Motor_Power",
 "Y_Motor_Torque", "Z_Axis_Actual_Feed_Rate_Override",
 "Z_Axis_Actual_Feed_Rate", "Z_Axis_Drive_Load",
 "Z_Axis_Perc_Feed_Override", "Z_Axis_Position",
 "Z_Axis_Rotary_Speed", "Z_Axis_Speed", "Z_Axis_Travel_Distance",
 "Z_Axis_Travel_Time", "Z_Motor_Current", "Z_Motor_Power",
 "Z_Motor_Torque", "A_Motor_Temperature", "C1_Motor_Temperature",
 "SPB1_Motor_Temperature", "X_Motor_Temperature",
 "Y_Motor_Temperature", "Z_Motor_Temperature"]


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
    # data = {"input": [{"message": prompt, "type": "user"}]}
    data = replace_keys(msgs)
    print(data)

    try:
        response = requests.post(base_url, json=data)
        response.raise_for_status()
        data = response.json()
        print('RISPOSTA: ', data)
        return data.get("output", "No response from the bot.")  # Extract the 'response' field
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"  # Return an error message in case of an exception

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
            if (message["role"] == 'assistant'):
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
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
        response = get_bot_response(prompt, st.session_state.messages)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.experimental_rerun()  # Force rerun to update the UI

    if st.button("Transfer variables"):
        send_to_chat()

if __name__ == "__main__":
    main()


