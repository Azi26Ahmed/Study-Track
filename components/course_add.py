import streamlit as st
from database import add_course
import datetime

def create_manual_section_form():
    """Form for manually creating course sections"""
    st.subheader("Manual Course Entry")
    
    title = st.text_input("Course Title")
    description = st.text_area("Course Description", height=100)
    platform = st.selectbox("Platform", ["udemy", "youtube", "other"])
    
    # Quick entry for large courses
    st.subheader("Quick Course Structure")
    col1, col2 = st.columns(2)
    with col1:
        num_sections = st.number_input("Number of Sections", min_value=1, value=1)
    with col2:
        avg_videos_per_section = st.number_input("Average Videos per Section", min_value=1, value=5)
        avg_duration = st.number_input("Average Video Duration (minutes)", min_value=1.0, value=10.0, step=0.5)
    
    use_quick_entry = st.checkbox("Use quick entry (for large courses)")
    
    sections = []
    
    if use_quick_entry:
        # Generate sections with estimated videos
        for i in range(int(num_sections)):
            videos = []
            for j in range(int(avg_videos_per_section)):
                videos.append({
                    "title": f"Video {j+1}",
                    "duration_minutes": avg_duration,
                    "duration_2x_minutes": round(avg_duration / 2, 1),
                    "completed": False
                })
            
            sections.append({
                "title": f"Section {i+1}",
                "videos": videos
            })
        
        st.info(f"Created {num_sections} sections with approximately {avg_videos_per_section} videos each. You can update video details as you progress through the course.")
    else:
        # Manual section-by-section entry
        for i in range(int(num_sections)):
            st.subheader(f"Section {i+1}")
            section_title = st.text_input(f"Section {i+1} Title", key=f"section_title_{i}")
            
            num_videos = st.number_input(f"Number of Videos in Section {i+1}", 
                                        min_value=1, value=1, key=f"num_videos_{i}")
            
            videos = []
            if num_videos > 10:
                # For many videos, offer simplified entry
                st.write(f"Section has {num_videos} videos. Using simplified entry.")
                for j in range(int(num_videos)):
                    videos.append({
                        "title": f"Video {j+1}",
                        "duration_minutes": avg_duration,
                        "duration_2x_minutes": round(avg_duration / 2, 1),
                        "completed": False
                    })
            else:
                # For fewer videos, allow detailed entry
                for j in range(int(num_videos)):
                    col1, col2 = st.columns(2)
                    with col1:
                        video_title = st.text_input(f"Video {j+1} Title", key=f"video_title_{i}_{j}")
                    with col2:
                        duration = st.number_input(f"Duration (minutes)", 
                                                min_value=0.0, value=avg_duration, step=0.5, 
                                                key=f"duration_{i}_{j}")
                    
                    videos.append({
                        "title": video_title,
                        "duration_minutes": duration,
                        "duration_2x_minutes": round(duration / 2, 1),
                        "completed": False
                    })
            
            sections.append({
                "title": section_title,
                "videos": videos
            })
    
    return {
        "title": title,
        "description": description,
        "platform": platform,
        "sections": sections
    }

def display_course_preview(course_data):
    """Display a preview of the course structure"""
    if not course_data:
        st.error("No course data to preview")
        return
    
    st.subheader("Course Preview")
    
    # Display basic course info
    st.write(f"**Title:** {course_data.get('title', 'Unknown Title')}")
    st.write(f"**Platform:** {course_data.get('platform', 'Unknown Platform').capitalize()}")
    
    # Display course statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Videos", course_data.get('total_videos', 0))
    with col2:
        st.metric("Total Duration", f"{course_data.get('total_duration_minutes', 0)} min")
    with col3:
        st.metric("Duration (2x)", f"{course_data.get('total_duration_2x_minutes', 0)} min")
    
    # For many sections, show summary instead of all details
    if len(course_data.get('sections', [])) > 10:
        st.write(f"**Course has {len(course_data.get('sections', []))} sections**")
        st.write("Showing first 3 sections as preview:")
        preview_sections = course_data.get('sections', [])[:3]
    else:
        preview_sections = course_data.get('sections', [])
    
    # Display sections and videos
    for i, section in enumerate(preview_sections):
        st.write(f"**Section {i+1}:** {section.get('title', 'Unknown Section')}")
        
        # Create a table for videos
        if section.get('videos'):
            video_count = len(section['videos'])
            if video_count > 10:
                st.write(f"Section contains {video_count} videos")
                video_data = []
                for j, video in enumerate(section['videos'][:5]):  # Show first 5 videos
                    video_data.append({
                        "Video": f"{j+1}. {video.get('title', 'Unknown Video')}",
                        "Duration": f"{video.get('duration_minutes', 0)} min",
                        "2x Duration": f"{video.get('duration_2x_minutes', 0)} min"
                    })
                if video_data:
                    st.table(video_data)
                st.write("... and more videos")
            else:
                video_data = []
                for j, video in enumerate(section['videos']):
                    video_data.append({
                        "Video": f"{j+1}. {video.get('title', 'Unknown Video')}",
                        "Duration": f"{video.get('duration_minutes', 0)} min",
                        "2x Duration": f"{video.get('duration_2x_minutes', 0)} min"
                    })
                if video_data:
                    st.table(video_data)
        else:
            st.write("No videos in this section")
    
    if len(course_data.get('sections', [])) > 3:
        st.write("... and more sections")

def add_course_form():
    """Form for adding a new course manually"""
    st.title("Add New Course")
    
    # Basic course information
    st.subheader("Course Details")
    
    course_title = st.text_input("Course Name", key="course_title")
    
    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("Category", ["Udemy", "YouTube", "Other"], key="platform")
    with col2:
        course_url = st.text_input("Course URL (optional)", key="course_url")
    
    course_description = st.text_area("Course Description (optional)", height=100, key="course_description")
    
    # Section configuration
    st.subheader("Course Structure")
    num_sections = st.number_input("Number of Sections", min_value=1, value=1, key="num_sections")
    
    # Container for dynamic section content
    section_container = st.container()
    
    # Submit button at the bottom
    submit_col1, submit_col2 = st.columns([1, 3])
    with submit_col1:
        submit_button = st.button("Save Course", use_container_width=True, key="save_course_btn")
    
    # Initialize or get sections from session state
    if "sections_data" not in st.session_state:
        st.session_state.sections_data = [{
            "title": f"Section {i+1}",
            "num_videos": 1,
            "videos": []
        } for i in range(int(num_sections))]
    
    # Update sections_data if number of sections changes
    if len(st.session_state.sections_data) != num_sections:
        # If increasing sections, add new ones
        if len(st.session_state.sections_data) < num_sections:
            for i in range(len(st.session_state.sections_data), int(num_sections)):
                st.session_state.sections_data.append({
                    "title": f"Section {i+1}",
                    "num_videos": 1,
                    "videos": []
                })
        # If decreasing sections, remove extra ones
        else:
            st.session_state.sections_data = st.session_state.sections_data[:int(num_sections)]
    
    # Display each section form
    with section_container:
        for i, section_data in enumerate(st.session_state.sections_data):
            with st.expander(f"Section {i+1}", expanded=(i == 0)):
                section_title = st.text_input(f"Section Title", 
                                            value=section_data["title"], 
                                            key=f"section_title_{i}")
                st.session_state.sections_data[i]["title"] = section_title
                
                num_videos = st.number_input(f"Number of Videos in Section {i+1}", 
                                          min_value=1, 
                                          value=section_data.get("num_videos", 1),
                                          key=f"num_videos_{i}")
                st.session_state.sections_data[i]["num_videos"] = num_videos
                
                # Videos information
                st.write("Video Information:")
                
                # Initialize or update videos list
                if not section_data.get("videos") or len(section_data["videos"]) != num_videos:
                    current_videos = section_data.get("videos", [])
                    # Preserve existing videos data when increasing
                    if len(current_videos) < num_videos:
                        for j in range(len(current_videos), int(num_videos)):
                            current_videos.append({
                                "title": f"Video {j+1}",
                                "duration_minutes": 10.0,
                                "duration_2x_minutes": 5.0,
                                "completed": False
                            })
                    else:
                        current_videos = current_videos[:int(num_videos)]
                    st.session_state.sections_data[i]["videos"] = current_videos
                
                # Display each video's information
                for j, video in enumerate(st.session_state.sections_data[i]["videos"]):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        video_title = st.text_input(f"Video {j+1} Title", 
                                               value=video.get("title", f"Video {j+1}"),
                                               key=f"video_title_{i}_{j}")
                        st.session_state.sections_data[i]["videos"][j]["title"] = video_title
                    
                    with col2:
                        duration = st.number_input(f"Duration (minutes)",
                                              min_value=0.5, 
                                              value=video.get("duration_minutes", 10.0),
                                              step=0.5,
                                              key=f"duration_{i}_{j}")
                        st.session_state.sections_data[i]["videos"][j]["duration_minutes"] = duration
                        st.session_state.sections_data[i]["videos"][j]["duration_2x_minutes"] = round(duration / 2, 1)
                
                # Add a separator between videos if there are many
                if num_videos > 3:
                    st.markdown("---")
    
    # Handle form submission
    if submit_button:
        if not course_title:
            st.error("Please enter a course title")
            return
        
        # Prepare course data
        sections = []
        for section_data in st.session_state.sections_data:
            sections.append({
                "title": section_data["title"],
                "videos": section_data["videos"]
            })
        
        # Calculate statistics
        total_videos = sum(len(section["videos"]) for section in sections)
        total_duration = sum(sum(video["duration_minutes"] for video in section["videos"]) for section in sections)
        
        course_data = {
            "title": course_title,
            "description": course_description,
            "platform": platform.lower(),
            "url": course_url,
            "sections": sections,
            "total_videos": total_videos,
            "completed_videos": 0,
            "completion_percentage": 0.0,
            "total_duration_minutes": round(total_duration, 1),
            "total_duration_2x_minutes": round(total_duration / 2, 1),
            "completed_duration_minutes": 0,
            "remaining_duration_minutes": round(total_duration, 1),
            "remaining_duration_2x_minutes": round(total_duration / 2, 1),
            "sections_completed": 0,
            "sections_total": len(sections)
        }
        
        # Add to database
        if "user" in st.session_state and st.session_state["user"]:
            user_id = st.session_state["user"]["id"]
            course_id = add_course(user_id, course_data)
            
            if course_id:
                st.success("Course added successfully!")
                # Clear session data
                st.session_state.pop("sections_data", None)
                # Redirect to courses page
                st.session_state["page"] = "courses"
                st.rerun()
            else:
                st.error("Failed to add course. It might already exist in your library.")
        else:
            st.error("You must be logged in to add courses")

    # Option to clear form
    if "sections_data" in st.session_state:
        if st.button("Clear Form", key="clear_form_btn"):
            st.session_state.pop("sections_data", None)
            st.rerun() 