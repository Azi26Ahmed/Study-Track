import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_course_statistics(course_data):
    """Calculate various statistics for a course"""
    if not course_data or 'sections' not in course_data:
        return {}
    
    total_videos = 0
    completed_videos = 0
    total_duration_minutes = 0
    completed_duration_minutes = 0
    
    for section in course_data['sections']:
        for video in section['videos']:
            total_videos += 1
            duration = video.get('duration_minutes', 0)
            total_duration_minutes += duration
            
            if video.get('completed', False):
                completed_videos += 1
                completed_duration_minutes += duration
    
    # Calculate statistics
    completion_percentage = (completed_videos / total_videos * 100) if total_videos > 0 else 0
    remaining_duration = total_duration_minutes - completed_duration_minutes
    remaining_duration_2x = remaining_duration / 2 if remaining_duration > 0 else 0
    sections_completed = sum(1 for section in course_data['sections'] 
                            if all(video.get('completed', False) for video in section['videos']))
    sections_total = len(course_data['sections'])
    
    return {
        "total_videos": total_videos,
        "completed_videos": completed_videos,
        "completion_percentage": round(completion_percentage, 1),
        "total_duration_minutes": round(total_duration_minutes, 1),
        "completed_duration_minutes": round(completed_duration_minutes, 1),
        "remaining_duration_minutes": round(remaining_duration, 1),
        "remaining_duration_2x_minutes": round(remaining_duration_2x, 1),
        "sections_completed": sections_completed,
        "sections_total": sections_total
    }

def update_course_statistics(course_data):
    """Update the course statistics in the course data object"""
    if not course_data or 'sections' not in course_data:
        return course_data
    
    stats = calculate_course_statistics(course_data)
    
    # Update the course data with the statistics
    for key, value in stats.items():
        course_data[key] = value
    
    return course_data 