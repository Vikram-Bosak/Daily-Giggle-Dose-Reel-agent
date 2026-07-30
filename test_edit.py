from src.agent_2_editor import process_video
video_data = {
    "id": "12345",
    "title": "Test Title",
    "local_path": "assets/fallback.mp4",
    "source": "Test Source"
}
res = process_video(video_data)
print(res)
