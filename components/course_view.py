import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from database import get_course_by_id, update_video_status, update_course
from components.course_handlers import calculate_course_statistics, update_course_statistics
import json

def display_course_header(course):
    """Display course title and platform badge"""
    # Get platform info for styling
    platform = course.get('platform', 'other').lower()
    platform_display = "YouTube" if platform == 'youtube' else "Udemy" if platform == 'udemy' else "Other"
    platform_icon = "🎬" if platform == 'youtube' else "🎓" if platform == 'udemy' else "📚"
    platform_color = "#FF0000" if platform == 'youtube' else "#A435F0" if platform == 'udemy' else "#4CAF50"
    
    # Custom CSS for header
    st.markdown("""
    <style>
    .course-header {
        margin-bottom: 20px;
    }
    .course-title {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .platform-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 15px;
        color: white;
        font-weight: bold;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display course title and platform badge
    st.markdown(f"""
    <div class="course-header">
        <div class="course-title">{course.get('title', 'Untitled Course')}</div>
        <div class="platform-badge" style="background-color: {platform_color};">
            {platform_icon} {platform_display}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Original URL button if available
    if 'url' in course and course['url'] and not course.get('url_generated', False):
        st.markdown(f"[View Original Course]({course['url']})")

def display_course_progress(course):
    """Display course progress metrics and visualizations"""
    # Calculate relevant statistics
    completion = course.get('completion_percentage', 0)
    total_videos = course.get('total_videos', 0)
    completed_videos = course.get('completed_videos', 0)
    total_sections = course.get('sections_total', 0)
    completed_sections = course.get('sections_completed', 0)
    remaining_duration = course.get('remaining_duration_minutes', 0)
    remaining_duration_2x = course.get('remaining_duration_2x_minutes', 0)
    total_duration = course.get('total_duration_minutes', 0)
    
    # Create a container for the progress section
    with st.container(border=True):
        st.markdown("### Course Progress")
        
        # Layout for visualizations
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Create gauge chart for completion percentage
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=completion,
                title={'text': "Completion", 'font': {'size': 20}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1},
                    'bar': {'color': "#4CAF50"},
                    'steps': [
                        {'range': [0, 33], 'color': "rgba(244, 67, 54, 0.2)"},
                        {'range': [33, 66], 'color': "rgba(255, 193, 7, 0.2)"},
                        {'range': [66, 100], 'color': "rgba(76, 175, 80, 0.2)"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': completion
                    }
                },
                number={'suffix': "%", 'font': {'size': 26}}
            ))
            fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Create pie chart showing completed vs remaining
            labels = ['Completed', 'Remaining']
            values = [completed_videos, total_videos - completed_videos]
            colors = ['#4CAF50', '#ECEFF1']
            
            fig = px.pie(
                values=values, 
                names=labels, 
                hole=0.6,
                color_discrete_sequence=colors
            )
            fig.update_layout(
                annotations=[dict(text=f"{completed_videos}/{total_videos}", x=0.5, y=0.5, font_size=20, showarrow=False)],
                showlegend=True,
                height=250,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Additional progress metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Videos", f"{completed_videos}/{total_videos}")
        
        with col2:
            st.metric("Sections", f"{completed_sections}/{total_sections}")
        
        with col3:
            st.metric("Time Remaining", f"{round(remaining_duration, 1)} min")
        
        with col4:
            st.metric("Time Remaining (2x)", f"{round(remaining_duration_2x, 1)} min")
            
        # Total duration
        st.metric("Total Duration", f"{round(total_duration, 1)} min")

def display_course_content(course, course_id):
    """Display course content with checkboxes for tracking video progress"""
    if not course.get('sections'):
        st.warning("This course doesn't have any content yet.")
        return
    
    # Custom CSS for content sections
    st.markdown("""
    <style>
    .section-header {
        background-color: #263238;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
        margin: 10px 0 5px 0;
        font-weight: bold;
    }
    .video-item {
        padding: 5px 10px;
        margin: 2px 0;
        border-radius: 3px;
        transition: background-color 0.2s;
    }
    .video-item:hover {
        background-color: #f5f5f5;
    }
    .video-duration {
        color: #757575;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Keep track if any updates were made
    update_made = False
    
    # Function to update video status
    def update_video_status(section_index, video_index, status):
        """Update video completion status in database"""
        # Make a deep copy of the course data to avoid session state issues
        updated_course = dict(course)
        # Update the video status
        updated_course['sections'][section_index]['videos'][video_index]['completed'] = status
        # Update statistics
        updated_course = update_course_statistics(updated_course)
        # Save to database
        update_course(course_id, updated_course)
        # Mark that we need to update the display
        nonlocal update_made
        update_made = True
        return updated_course
    
    # Display each section and its videos
    for section_index, section in enumerate(course.get('sections', [])):
        st.markdown(f"""
        <div class="section-header">
            {section.get('title', f'Section {section_index + 1}')}
        </div>
        """, unsafe_allow_html=True)
        
        # Display videos in this section
        for video_index, video in enumerate(section.get('videos', [])):
            video_title = video.get('title', f'Video {video_index + 1}')
            duration = video.get('duration_minutes', 0)
            is_completed = video.get('completed', False)
            
            # Create unique key for checkbox
            key = f"video_{section_index}_{video_index}_{course_id}"
            
            col1, col2 = st.columns([9, 1])
            
            with col1:
                st.markdown(f"""
                <div class="video-item">
                    {video_title}
                    <span class="video-duration"> - {duration} min</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Checkbox to mark video as completed/not completed - Fix empty label issue
                if st.checkbox("Completed", value=is_completed, key=key, label_visibility="collapsed"):
                    if not is_completed:
                        # Update status to completed
                        course = update_video_status(section_index, video_index, True)
                else:
                    if is_completed:
                        # Update status to not completed
                        course = update_video_status(section_index, video_index, False)
    
    # If any video status was updated, get the latest data and rerun to refresh the UI
    if update_made:
        st.rerun()

def display_course_info_tab(course, course_id):
    """Display course description and content"""
    # Display description if available
    if course.get('description'):
        with st.expander("Course Description", expanded=True):
            st.write(course.get('description', ''))
    
    # Display course content for tracking progress
    display_course_content(course, course_id)

def display_statistics_tab(course):
    """Display statistics tab with completion rates"""
    st.header("Course Statistics")
    
    # Get statistics
    stats = calculate_course_statistics(course)
    
    # Display course completion
    st.subheader("Course Completion")
    
    # Create columns for the charts
    col1, col2 = st.columns(2)
    
    # Completion percentage (gauge chart)
    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=stats['completion_percentage'],
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
                    'value': stats['completion_percentage']
                }
            }
        ))
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    # Video completion breakdown (pie chart)
    with col2:
        fig = go.Figure(data=[go.Pie(
            labels=['Completed', 'Remaining'],
            values=[stats['completed_videos'], stats['total_videos'] - stats['completed_videos']],
            hole=.4,
            marker_colors=['#4CAF50', '#E0E0E0']
        )])
        fig.update_layout(
            title_text="Video Completion",
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Time statistics
    st.subheader("Time Statistics")
    
    col1, col2 = st.columns(2)
    
    # Time completion chart
    with col1:
        labels = ['Watched', 'Remaining']
        values = [stats['completed_duration_minutes'], stats['remaining_duration_minutes']]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.4,
            marker_colors=['#2196F3', '#E0E0E0']
        )])
        fig.update_layout(
            title_text="Time Spent vs Remaining",
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Remaining time visualization
    with col2:
        remaining_regular = stats['remaining_duration_minutes']
        remaining_speed_2x = stats['remaining_duration_2x_minutes']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=['Regular Speed', '2x Speed'],
            x=[remaining_regular, remaining_speed_2x],
            orientation='h',
            marker=dict(
                color=['#FF9800', '#2196F3'],
                line=dict(color='rgba(0, 0, 0, 0)', width=1)
            ),
            text=[f"{round(remaining_regular, 1)} min", f"{round(remaining_speed_2x, 1)} min"],
            textposition='inside',
            name='Time'
        ))
        
        fig.update_layout(
            title='Time to Complete',
            xaxis=dict(title='Minutes'),
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Section completion statistics
    if 'sections' in course and course['sections']:
        st.subheader("Section Completion")
        
        # Prepare data for the section completion chart
        section_names = []
        section_percentages = []
        
        # Sort sections to be in ascending order by section number (section 1 first)
        sorted_sections = sorted(course['sections'], key=lambda x: x.get('order', 0))
        
        for section in sorted_sections:
            section_name = section.get('title', 'Unknown Section')
            videos = section.get('videos', [])
            completed = sum(1 for video in videos if video.get('completed', False))
            total = len(videos)
            
            if total > 0:
                completion_percentage = round((completed / total) * 100, 1)
            else:
                completion_percentage = 0
                
            section_names.append(section_name)
            section_percentages.append(completion_percentage)
            
        # For vertical charts, we need to reverse the lists so section 1 appears at the top
        section_names.reverse()
        section_percentages.reverse()
        
        # Create the section completion bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=section_percentages,
            y=section_names,
            orientation='h',
            marker_color=['#4CAF50' if p >= 75 else '#FF9800' if p >= 25 else '#F44336' for p in section_percentages],
            text=[f"{p}%" for p in section_percentages],
            textposition='auto',
        ))
        
        fig.update_layout(
            title='Section Completion Percentage',
            xaxis=dict(title='Completion Percentage', range=[0, 100]),
            yaxis=dict(title='Section'),
            height=max(400, 50 * len(section_names)),
            margin=dict(l=20, r=20, t=50, b=20),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No section data available for this course.")

def course_view(course_id):
    """Display a course view with tabs for course info and statistics"""
    # Get course data from database
    course = get_course_by_id(course_id)
    
    if not course:
        st.error("Course not found!")
        return
    
    # Store course ID in session state for component communication
    if "current_course_id" not in st.session_state:
        st.session_state["current_course_id"] = course_id
    
    # Display course header
    display_course_header(course)
    
    # Display course progress visualization
    display_course_progress(course)
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Course Content", "Statistics"])
    
    with tab1:
        display_course_info_tab(course, course_id)
    
    with tab2:
        display_statistics_tab(course)

def course_list_view(courses):
    """Display a list of courses sorted by completion percentage"""
    if not courses:
        st.info("You haven't added any courses yet.")
        st.markdown("Use the sidebar to navigate to 'Add New Course' page.")
        return
    
    # Sort courses by completion percentage (descending)
    sorted_courses = sorted(
        courses,
        key=lambda x: x.get('completion_percentage', 0),
        reverse=True
    )
    
    # Display in a grid layout with improved styling
    st.markdown("""
    <style>
    .course-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
    }
    .course-card {
        background-color: #f9f9f9;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .course-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .course-list-title {
        font-size: 20px;
        font-weight: bold;
        color: #263238;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display courses in a grid
    cols = st.columns(3)
    
    for i, course in enumerate(sorted_courses):
        with cols[i % 3]:
            with st.container(border=True):
                # Course title and completion with better styling
                st.markdown(f"""
                <div class="course-list-title">{course.get('title', 'Untitled Course')}</div>
                """, unsafe_allow_html=True)
                
                # Display platform
                platform = course.get('platform', 'other')
                if platform == 'youtube':
                    st.markdown("🎬 YouTube")
                elif platform == 'udemy':
                    st.markdown("🎓 Udemy")
                else:
                    st.markdown("📚 Other")
                
                # Progress bar
                completion = course.get('completion_percentage', 0)
                st.progress(completion / 100, text=f"{completion}% complete")
                
                # Course stats
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Videos: {course.get('completed_videos', 0)}/{course.get('total_videos', 0)}")
                with col2:
                    st.write(f"Sections: {course.get('sections_completed', 0)}/{course.get('sections_total', 0)}")
                
                # Time stats
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Remaining: {round(course.get('remaining_duration_minutes', 0), 1)} min")
                with col2:
                    st.write(f"At 2x: {round(course.get('remaining_duration_2x_minutes', 0), 1)} min")
                
                # Total time
                st.write(f"Total Time: {round(course.get('total_duration_minutes', 0), 1)} min")
                
                # View button
                if st.button("View Details", key=f"view_details_{course['_id']}", use_container_width=True):
                    st.session_state["selected_course"] = str(course["_id"])
                    st.rerun() 