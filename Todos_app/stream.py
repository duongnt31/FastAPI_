import streamlit as st
import requests

# FastAPI endpoint
api_base_url = 'http://0.0.0.0:8000'  # Update this URL to match your FastAPI service

# Page configuration
st.set_page_config(page_title="Todo Service", page_icon="✅", layout="centered")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Register", "Login", "View All Todos", "View Todo", 
    "Create Todo", "Update Todo", "Delete Todo", 
    "Admin View All Todos", "Admin Delete Todo", 
    "View User", "Change Password", "Change Phone Number"
])

# Helper function to get authentication token
def get_token():
    return st.session_state.get("token")

# Helper function to set authentication token
def set_token(token):
    st.session_state["token"] = token

# Registration page
if page == "Register":
    st.title("Register New User")

    username = st.text_input("Username")
    email = st.text_input("Email")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    password = st.text_input("Password", type="password")
    role = st.text_input("Role")
    phone_number = st.text_input("Phone Number")

    if st.button("Register"):
        if username and email and first_name and last_name and password and role and phone_number:
            user_data = {
                "username": username,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
                "role": role,
                "phone_number": phone_number
            }

            response = requests.post(f"{api_base_url}/auth/", json=user_data)
            if response.status_code == 201:
                st.success("User registered successfully")
            else:
                st.error("An error occurred during registration")
        else:
            st.warning("Please fill in all fields")

# Login page
elif page == "Login":
    st.title("User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            form_data = {
                "username": username,
                "password": password
            }

            response = requests.post(f"{api_base_url}/auth/token", data=form_data)
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get("access_token")
                set_token(access_token)
                st.success(f"Login successful! Access token: {access_token}")
            else:
                st.error("Invalid username or password")
        else:
            st.warning("Please fill in all fields")

# View all todos page
elif page == "View All Todos":
    st.title("View All Todos")

    token = get_token()
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{api_base_url}/todos", headers=headers)
        if response.status_code == 200:
            todos = response.json()
            st.write(todos)
        else:
            st.error("Failed to fetch todos")
    else:
        st.warning("Please login first")

# View specific todo page
elif page == "View Todo":
    st.title("View Todo")

    token = get_token()
    todo_id = st.number_input("Todo ID", min_value=1, step=1)

    if st.button("View Todo"):
        if token:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{api_base_url}/todos/{todo_id}", headers=headers)
            if response.status_code == 200:
                todo = response.json()
                st.write(todo)
            else:
                st.error("Failed to fetch todo")
        else:
            st.warning("Please login first")

# Create todo page
elif page == "Create Todo":
    st.title("Create Todo")

    token = get_token()
    title = st.text_input("Title")
    description = st.text_input("Description")
    priority = st.number_input("Priority", min_value=1, max_value=5, step=1)
    complete = st.checkbox("Complete")

    if st.button("Create Todo"):
        if token:
            headers = {"Authorization": f"Bearer {token}"}
            todo_data = {
                "title": title,
                "description": description,
                "priority": priority,
                "complete": complete
            }
            response = requests.post(f"{api_base_url}/todos/create", json=todo_data, headers=headers)
            if response.status_code == 201:
                st.success("Todo created successfully")
            else:
                st.error("Failed to create todo")
        else:
            st.warning("Please login first")

# Update todo page
elif page == "Update Todo":
    st.title("Update Todo")

    token = get_token()
    todo_id = st.number_input("Todo ID", min_value=1, step=1)
    title = st.text_input("Title")
    description = st.text_input("Description")
    priority = st.number_input("Priority", min_value=1, max_value=5, step=1)
    complete = st.checkbox("Complete")

    if st.button("Update Todo"):
        if token:
            headers = {"Authorization": f"Bearer {token}"}
            todo_data = {
                "title": title,
                "description": description,
                "priority": priority,
                "complete": complete
            }
            response = requests.put(f"{api_base_url}/todos/{todo_id}", json=todo_data, headers=headers)
            if response.status_code == 204:
                st.success("Todo updated successfully")
            else:
                st.error("Failed to update todo")
        else:
            st.warning("Please login first")

# Delete todo page
elif page == "Delete Todo":
    st.title("Delete Todo")

    token = get_token()
    todo_id = st.number_input("Todo ID", min_value=1, step=1)

    if st.button("Delete Todo"):
        if token:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.delete(f"{api_base_url}/todos/{todo_id}", headers=headers)
            if response.status_code == 204:
                st.success("Todo deleted successfully")
            else:
                st.error("Failed to delete todo")
        else:
            st.warning("Please login first")

# Admin view all todos page
elif page == "Admin View All Todos":
    st.title("Admin View All Todos")

    token = get_token()
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{api_base_url}/admin/todos", headers=headers)
        if response.status_code == 200:
            todos = response.json()
            st.write(todos)
        else:
            st.error("Failed to fetch todos")
    else:
        st.warning("Please login first")

# Admin delete todo page
elif page == "Admin Delete Todo":
    st.title("Admin Delete Todo")

    token = get_token()
    todo_id = st.number_input("Todo ID", min_value=1, step=1)

    if st.button("Delete Todo"):
        if token:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.delete(f"{api_base_url}/admin/todos/{todo_id}", headers=headers)
            if response.status_code == 204:
                st.success("Todo deleted successfully")
            else:
                st.error("Failed to delete todo")
        else:
            st.warning("Please login first")

# View user details page
elif page == "View User":
    st.title("View User")

    token = get_token()
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{api_base_url}/user/todos", headers=headers)
        if response.status_code == 200:
            user = response.json()
            st.write(user)
        else:
            st.error("Failed to fetch user details")
    else:
        st.warning("Please login first")

# Change password page
elif page == "Change Password":
    st.title("Change Password")

    token = get_token()
    current_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")

    if st.button("Change Password"):
        if token:
            headers = {"Authorization": f"Bearer {token}"}
            password_data = {
                "password": current_password,
                "new_password": new_password
            }
            response = requests.put(f"{api_base_url}/user/password", json=password_data, headers=headers)
            if response.status_code == 204:
                st.success("Password changed successfully")
            else:
                st.error("Failed to change password")
        else:
            st.warning("Please login first")

# Change phone number page
elif page == "Change Phone Number":
    st.title("Change Phone Number")

    token = get_token()
    phone_number = st.text_input("New Phone Number")

    if st.button("Change Phone Number"):
        if token:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.put(f"{api_base_url}/user/phone_number/{phone_number}", headers=headers)
            if response.status_code == 204:
                st.success("Phone number changed successfully")
            else:
                st.error("Failed to change phone number")
        else:
            st.warning("Please login first")
