from time import time
import requests

def test_batch(comments):
    """Test multiple comments at once (batch mode)."""
    response = requests.post(
        "http://10.51.33.33:5000/getsentiment",
        json=comments
    )
    result = response.json()
    print("Batch Results:\n")
    for key, value in result.items():
        print(f"{key}: {comments[key]}")
        print(f"Sentiment: {value}")
        print("-" * 50)


# Run tests
print("Testing batch API...\n")

batch_comments = {
    "0": "Took ownership and responsibility early for the project. Took initiative. Came up with good suggestions and ideas on how to tackle problems and achieve goals. Assisted with documentation and many of the backend changes required for the project.",
    "1": "Andrew’s technical skills are exceptional, and he was able to contribute a fair amount to the project. His people skills and attitude towards other people still need a bit of work though. Early in the project I thought I might be a bit of a problem for the group however this perception changed a bit towards the end. He is a team member who just needs tasks to do to feel comfortable in the project. As Andrew matures more in the IT field, I feel he will become an excellent team contributor in the workforce.",
    "2": "Her contribution to the project was significantly below expectations across multiple areas. Her cooperation with the team was consistently poor - she frequently declined participation in team meetings and activities, claiming she had other commitments, which made coordination extremely difficult for the rest of us. As our communications officer, she failed to take initiative in her role, requiring constant reminders and spoon-feeding of information before sending any correspondence. Even when reminded multiple times, her response was often delayed or inadequate. Sara showed reluctance to address even minor errors independently, preferring to wait for other team members to be available rather than taking personal responsibility for fixes. Her lack of proactive engagement and unwillingness to go beyond the absolute minimum requirements created additional workload for other team members. While she managed to deliver some work on time, her overall approach was passive and uncooperative. Salwa would need to significantly improve her initiative, responsibility, and team collaboration skills to be an effective contributor in future group projects.",
    "3": "He did a great job throughout the entire project. He handled the team well and made sure the project was completed within the limited time. It was impressive to see him build the backend of the app so smoothly. He also helped us understand the backend and frontend flow, which made it easier to know how the app works. He taught the non-developers how to use POSTMAN so we could do the testing properly. He contributed a lot and stayed dedicated to the project. He also corrected us when needed and proofread the documents.",
    "4": "Soniya has joined the team by week 3, but she worked on her parts without any complaints. She led the documentation team and assigned "
}

start_time = time()
test_batch(batch_comments)
end_time = time()

print(f"Batch API request took {end_time - start_time} seconds.")