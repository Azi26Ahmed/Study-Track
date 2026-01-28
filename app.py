import streamlit as st
from components.auth import auth_page, require_auth
from components.dashboard import dashboard
from components.course_add import add_course_form
from components.course_view import course_view, course_list_view
from database import get_user_courses

# Set page config
st.set_page_config(
    page_title="Study Track",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
    }
    footer {visibility: hidden;}
    .app-header {
        color: #212121;
        padding: 1rem;
        margin-bottom: 1.5rem;
        text-align: center;
        border-bottom: 1px solid #e0e0e0;
    }
    .app-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: bold;
        color: white;
    }
    .app-header p {
        margin: 5px 0 0 0;
        font-size: 1rem;
        color: white;
    }
    /* Remove blue outline from containers */
    [data-testid="stHorizontalBlock"] > div[data-testid="column"] > div[data-testid="stContainer"] {
        border: none !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
    }
    /* Customize sidebar */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E !important;
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        background-color: #1E1E1E !important;
    }
</style>
""", unsafe_allow_html=True)

def display_header():
    """Display the app header on all pages"""
    st.markdown("""
    <div class="app-header">
        <h1>Study Track</h1>
        <p>Track your progress and boost your learning</p>
    </div>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if "page" not in st.session_state:
        st.session_state["page"] = "dashboard"

def sidebar_navigation():
    """Create sidebar navigation"""
    # Remove the titles from sidebar as requested
    
    # Only show navigation when authenticated
    if st.session_state["authenticated"] and "user" in st.session_state:
        # User info
        st.sidebar.markdown(f"**Logged in as:** {st.session_state['user']['name']}")
        
        # Navigation buttons without the "Navigation" header
        if st.sidebar.button("Dashboard", key="sidebar_dashboard_btn", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
            
        if st.sidebar.button("My Courses", key="sidebar_courses_btn", use_container_width=True):
            st.session_state["page"] = "courses"
            st.rerun()
            
        if st.sidebar.button("Add New Course", key="sidebar_add_course_btn", use_container_width=True):
            st.session_state["page"] = "add_course"
            st.rerun()
        
        # Logout option
        st.sidebar.markdown("---")
        if st.sidebar.button("Logout", key="sidebar_logout_btn", use_container_width=True):
            st.session_state["authenticated"] = False
            st.session_state.pop("user", None)
            st.session_state["page"] = "dashboard"
            st.rerun()

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Display the header on all pages (including login)
    display_header()
    
    # Display sidebar only if authenticated
    if st.session_state["authenticated"]:
        sidebar_navigation()
    else:
        # Hide sidebar for login screen
        st.markdown("""
        <style>
        [data-testid="stSidebar"] {display: none;}
        </style>
        """, unsafe_allow_html=True)
    
    # Authentication required
    if not st.session_state["authenticated"]:
        auth_page()
        return
    
    # Page router
    current_page = st.session_state["page"]
    
    if current_page == "dashboard":
        dashboard(st.session_state["user"])
    
    elif current_page == "courses":
        st.title("My Courses")
        courses = get_user_courses(st.session_state["user"]["id"])
        
        if "selected_course" in st.session_state:
            # Single course view
            course_view(st.session_state["selected_course"])
            
            # Back button
            if st.button("Back to All Courses", key="back_to_courses_btn"):
                st.session_state.pop("selected_course", None)
                st.rerun()
        else:
            # Course list view
            course_list_view(courses)
    
    elif current_page == "add_course":
        add_course_form()

if __name__ == "__main__":
    main() 