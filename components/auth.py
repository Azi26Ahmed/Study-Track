import streamlit as st
import re
from database import create_user, get_user_by_email, verify_password

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_strong_password(password):
    """Check if password meets minimum requirements"""
    # At least 8 characters, 1 uppercase, 1 lowercase, 1 number
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True

def login_form():
    """Display login form and handle login"""
    # Create a centered container with styling
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.subheader("Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if not email or not password:
                    st.error("Please fill in all fields")
                    return False
                    
                user = get_user_by_email(email)
                if not user:
                    st.error("Email not found. Please sign up first.")
                    return False
                    
                if not verify_password(user["password"], password):
                    st.error("Incorrect password")
                    return False
                    
                # Login successful
                st.success("Login successful!")
                st.session_state["user"] = {
                    "id": str(user["_id"]),
                    "email": user["email"],
                    "name": user["name"]
                }
                st.session_state["authenticated"] = True
                return True
                
    return False

def signup_form():
    """Display signup form and handle registration"""
    # Create a centered container with styling
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("signup_form"):
            st.subheader("Sign Up")
            name = st.text_input("Name", key="signup_name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
            
            # Password strength indicator
            if password:
                if is_strong_password(password):
                    st.success("Strong password")
                else:
                    st.warning("Password should be at least 8 characters with uppercase, lowercase and numbers")
            
            submit = st.form_submit_button("Sign Up", use_container_width=True)
            
            if submit:
                if not name or not email or not password or not confirm_password:
                    st.error("Please fill in all fields")
                    return False
                    
                if not is_valid_email(email):
                    st.error("Please enter a valid email")
                    return False
                    
                if password != confirm_password:
                    st.error("Passwords do not match")
                    return False
                    
                if not is_strong_password(password):
                    st.error("Password does not meet security requirements")
                    return False
                    
                # Check if email already exists
                existing_user = get_user_by_email(email)
                if existing_user:
                    st.error("Email already exists")
                    return False
                    
                # Create new user
                user_id = create_user(email, password, name)
                if user_id:
                    st.success("Sign up successful! Please log in.")
                    return True
                else:
                    st.error("Error creating user. Please try again.")
                    return False
                
    return False

def auth_page():
    """Main authentication page with tabs for login and signup"""
    # Add custom CSS for better styling of the auth page
    st.markdown("""
    <style>
    .auth-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 20px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0 0;
        font-weight: 500;
    }
    /* Add more spacing between tabs */
    .stTabs [data-baseweb="tab-panel"] {
        margin-top: 20px;
    }
    /* Login-signup divider */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 1px solid #ddd;
        padding-bottom: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        margin-right: 10px;
    }
    .auth-header {
        text-align: center;
        margin-bottom: 20px;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        
    if st.session_state["authenticated"]:
        # If already logged in, show logout option
        if st.button("Logout"):
            st.session_state["authenticated"] = False
            st.session_state.pop("user", None)
            st.rerun()
        return True
    
    # Use columns to center the auth forms
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Add some padding
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # Display header text above tabs
        st.markdown("<h2 class='auth-header'>Login or Sign Up</h2>", unsafe_allow_html=True)
        
        # Show login/signup tabs
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            if login_form():
                st.rerun()
                
        with tab2:
            if signup_form():
                # Switch to login tab after successful signup
                st.rerun()
                
    return st.session_state["authenticated"]

def require_auth():
    """Function to require authentication before accessing a page"""
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.warning("Please log in to access this page")
        auth_page()
        return False
    return True 