import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import get_user_courses, delete_course

def display_user_welcome(user):
    """Display welcome message for the user"""
    # Removed the welcome message as requested
    pass

def display_overall_stats(courses):
    """Display overall statistics for all courses"""
    if not courses:
        return
    
    # Collect statistics
    total_courses = len(courses)
    total_videos = sum(course.get('total_videos', 0) for course in courses)
    completed_videos = sum(course.get('completed_videos', 0) for course in courses)
    total_duration = sum(course.get('total_duration_minutes', 0) for course in courses)
    completed_duration = sum(course.get('completed_duration_minutes', 0) for course in courses if 'completed_duration_minutes' in course)
    
    # Calculate overall completion percentage
    overall_completion = 0
    if total_videos > 0:
        overall_completion = round(completed_videos / total_videos * 100, 1)
    
    # Create a more graphical representation with cards and gauges
    st.markdown("""
    <style>
    .stats-card {
        background-color: #263238;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        height: 100%;
    }
    .stats-card h3 {
        color: #f1f1f1;
        font-size: 16px;
        margin-bottom: 10px;
    }
    .stats-card .value {
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display stats in a grid with colorful cards
    col1, col2, col3 = st.columns(3)
    
    # Courses count and completion gauge
    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=overall_completion,
            title={'text': "Overall Completion"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#4CAF50"},
                'steps': [
                    {'range': [0, 33], 'color': "#EF5350"},
                    {'range': [33, 66], 'color': "#FFCA28"},
                    {'range': [66, 100], 'color': "#66BB6A"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 2},
                    'thickness': 0.75,
                    'value': overall_completion
                }
            }
        ))
        fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div class="stats-card">
            <h3>Total Courses</h3>
            <div class="value">{total_courses}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Videos progress
    with col2:
        # Videos completion chart
        fig = go.Figure(go.Indicator(
            mode="number+gauge",
            value=completed_videos,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Videos Completed"},
            gauge={
                'axis': {'range': [0, total_videos], 'tickwidth': 1},
                'bar': {'color': "#4CAF50"},
                'bgcolor': "lightgray",
                'borderwidth': 2,
                'steps': [
                    {'range': [0, total_videos/2], 'color': 'rgba(76, 175, 80, 0.3)'},
                    {'range': [total_videos/2, total_videos], 'color': 'rgba(76, 175, 80, 0.6)'}
                ],
            },
            number={'suffix': f"/{total_videos}"}
        ))
        fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    # Time remaining stats
    with col3:
        remaining_duration = total_duration - completed_duration
        remaining_duration_2x = remaining_duration / 2
        
        # Create a visual representation of time remaining
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=['Regular Speed', '2x Speed'],
            x=[remaining_duration, remaining_duration_2x],
            orientation='h',
            marker=dict(
                color=['#FF9800', '#2196F3'],
                line=dict(color='rgba(0, 0, 0, 0)', width=1)
            ),
            text=[f"{round(remaining_duration, 1)} min", f"{round(remaining_duration_2x, 1)} min"],
            textposition='inside',
            name='Time'
        ))
        
        fig.update_layout(
            title='Time Remaining',
            xaxis=dict(title='Minutes'),
            height=200,
            margin=dict(l=20, r=20, t=50, b=20),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

def display_course_summary(courses):
    """Display summary of all courses with their progress"""
    if not courses:
        st.info("You haven't added any courses yet. Click 'Add Course' to get started!")
        return
    
    # Display courses in a grid with delete buttons
    st.subheader("My Courses")
    
    # Add custom styling for course cards
    st.markdown("""
    <style>
        .course-card {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            padding: 15px;
            height: 100%;
            transition: transform 0.3s ease;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        }
        .course-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        .course-title {
            font-weight: bold;
            font-size: 20px;
            color: #000000;
            margin-bottom: 10px;
            background-color: rgba(255, 255, 255, 0.7);
            padding: 5px;
            border-radius: 4px;
            display: inline-block;
        }
        .platform-badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
            margin-bottom: 12px;
        }
        .progress-container {
            margin: 10px 0;
        }
        .progress-stat {
            margin: 5px 0;
            font-size: 14px;
        }
        .completion-value {
            font-weight: bold;
            color: #263238;
        }
        .action-buttons {
            margin-top: 10px;
            display: flex;
            justify-content: space-between;
        }
    </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(3)
    
    for i, course in enumerate(courses):
        col = cols[i % 3]
        
        with col:
            # Get platform information and styling
            platform = course.get('platform', 'other').lower()
            platform_display = "YouTube" if platform == 'youtube' else "Udemy" if platform == 'udemy' else "Other"
            platform_icon = "🎬" if platform == 'youtube' else "🎓" if platform == 'udemy' else "📚"
            platform_color = "#FF0000" if platform == 'youtube' else "#A435F0" if platform == 'udemy' else "#4CAF50"
            
            # Calculate completion values
            completion = course.get('completion_percentage', 0)
            total_videos = course.get('total_videos', 0)
            completed_videos = course.get('completed_videos', 0)
            total_sections = course.get('sections_total', 0)
            completed_sections = course.get('sections_completed', 0)
            total_duration = course.get('total_duration_minutes', 0)
            remaining_duration = course.get('remaining_duration_minutes', 0)
            remaining_2x = course.get('remaining_duration_2x_minutes', 0)
            
            # Create a bordered container similar to course progress style
            with st.container(border=True):
                # Course title and platform with custom styling
                st.markdown(f"""
                <div class="course-title">{course.get('title', 'Untitled Course')}</div>
                <div class="platform-badge" style="background-color: {platform_color}; color: white;">
                    {platform_icon} {platform_display}
                </div>
                """, unsafe_allow_html=True)
                
                # Progress visualization with improved styling
                progress_color = "#4CAF50" if completion >= 75 else "#FF9800" if completion >= 25 else "#F44336"
                st.progress(completion / 100, text=f"{completion}% complete")
                
                # Course stats with better layout
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div class="progress-stat">
                        <span>Videos:</span> <span class="completion-value">{completed_videos}/{total_videos}</span>
                    </div>
                    <div class="progress-stat">
                        <span>Sections:</span> <span class="completion-value">{completed_sections}/{total_sections}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="progress-stat">
                        <span>Remaining:</span> <span class="completion-value">{round(remaining_duration, 1)} min</span>
                    </div>
                    <div class="progress-stat">
                        <span>At 2x:</span> <span class="completion-value">{round(remaining_2x, 1)} min</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="progress-stat" style="text-align: center; margin-top: 5px;">
                    <span>Total Time:</span> <span class="completion-value">{round(total_duration, 1)} min</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("View Course", key=f"view_{course['_id']}", use_container_width=True):
                        st.session_state["selected_course"] = str(course["_id"])
                        st.session_state["page"] = "courses"
                        st.rerun()
                with col2:
                    if st.button("Delete", key=f"delete_{course['_id']}", use_container_width=True):
                        if delete_course(str(course["_id"])):
                            st.success("Course deleted successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to delete course")

def display_platform_distribution(courses):
    """Display platform distribution pie chart"""
    if not courses or len(courses) == 0:
        return
    
    # Count courses by platform
    platform_counts = {}
    for course in courses:
        platform = course.get('platform', 'other').capitalize()
        platform_counts[platform] = platform_counts.get(platform, 0) + 1
    
    if platform_counts:
        # Create pie chart with improved styling
        fig = px.pie(
            values=list(platform_counts.values()),
            names=list(platform_counts.keys()),
            title='Courses by Platform',
            color_discrete_map={
                'Youtube': '#FF0000',
                'Udemy': '#A435F0',
                'Other': '#4CAF50'
            }
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(l=20, r=20, t=50, b=20),
        )
        
        st.plotly_chart(fig, use_container_width=True)

def dashboard(user):
    """Main dashboard function"""
    # Get all user courses
    courses = get_user_courses(user['id'])
    
    # Display welcome section - removed as requested
    # display_user_welcome(user)
    
    # Display overall stats
    st.subheader("Your Learning Stats")
    display_overall_stats(courses)
    
    # Display courses with delete functionality
    display_course_summary(courses)
    
    # Display platform distribution chart
    if courses:
        display_platform_distribution(courses)
    
    # Action button to add new course
    st.subheader("Actions")
    
    if st.button("Add New Course", key="dashboard_add_course_btn", use_container_width=True):
        st.session_state["page"] = "add_course"
        st.rerun() 