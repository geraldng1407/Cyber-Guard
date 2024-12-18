import httpx
import random
import asyncio

# Target URLs for login, password reset, and fetching fake users
LOGIN_URL = "http://localhost:8058/login"
PASSWORD_RESET_URL = "http://localhost:8058/forget_password"
FAKE_USERS_URL = "http://localhost:8058/fake_users"

# Function to get fake users from the FastAPI app
async def get_fake_users():
    async with httpx.AsyncClient() as client:
        response = await client.get(FAKE_USERS_URL)
        return response.json()

# Function to attempt login for a user
async def login_user(user):
    async with httpx.AsyncClient() as client:
        response = await client.post(LOGIN_URL, json=user)
        return response

# Function to simulate password reset
async def initiate_password_reset(username):
    async with httpx.AsyncClient() as client:
        response = await client.post(PASSWORD_RESET_URL, json={"username": username})
        return response

# Simulate a user's login behavior
async def simulate_user_login(username, password, attempts):
    while True:
        print("simulate_user_login")
        brute_force = True
        if not brute_force:
        
            # Randomize whether to use correct or incorrect password
            is_correct_password = random.choice([True, False])

            # Set correct or wrong password
            user = {
                "username": username,
                "password": password if is_correct_password or attempts[username] >= 3 else "wrongpassword"
            }

            # Attempt to log in
            response = await login_user(user)

            if response.status_code == 200:
                # If login succeeds, print success and reset attempts counter
                print(f"Successful login for {username}: {response.json()}")
                attempts[username] = 0
            else:
                # If login fails, increment attempts counter
                print(f"Failed login for {username}: {response.json()}")
                attempts[username] += 1

            # If too many failed attempts, trigger password reset
            if attempts[username] >= random.randint(1, 5):
                print(f"{username} failed login {attempts[username]} times. Initiating password reset...")
                reset_response = await initiate_password_reset(username)
                if reset_response.status_code == 200:
                    print(f"Password reset successful for {username}")
                else:
                    print(f"Password reset failed for {username}: {reset_response.json()}")
                attempts[username] = 0  # Reset attempts

            # Random sleep to simulate human-like behavior between attempts
            # await asyncio.sleep(random.uniform(1, 3))
        else:
            user = {
            "username": username,
            "password": "wrong_password"
            }
            print("simulate_user_login")
            # Assign probabilities
            reset_probability = 0.01

            if random.random() < reset_probability:
                # Trigger password reset
                reset_response = await initiate_password_reset(username)
                if reset_response.status_code == 200:
                    print(f"Password reset successful for {username}")
                else:
                    print(f"Password reset failed for {username}: {reset_response.json()}")
            else:
                # Attempt to login
                response = await login_user(user)
                if response.status_code == 200:
                    # If login succeeds, print success
                    print(f"Successful login for {username}: {response.json()}")
                    # Reset attempts counter (if any)
                    # attempts[username] = 0
                else:
                    # If login fails, increment attempts counter (if any)
                    print(f"Failed login for {username}: {response.json()}")
                    # attempts[username] += 1

            

# Simulate multiple concurrent users logging in and interacting
async def simulate_traffic(fake_users):
    attempts = {username: 0 for username in fake_users}  # Track failed login attempts for each user
    
    # Create a list of tasks where each task simulates a user logging in
    tasks = []
    for username, user_data in fake_users.items():
        task = simulate_user_login(username, user_data["password"], attempts)
        tasks.append(task)

    # Run all tasks concurrently, simulating mixed user logins
    await asyncio.gather(*tasks)

# Main function to orchestrate the entire simulation
async def main():
    fake_users = await get_fake_users()  # Fetch fake users from the API
    print(fake_users)
    start_time = asyncio.get_event_loop().time()
    end_time = start_time + 1680000  # 3 minutes in seconds

    # Create a task to run the simulation
    simulation_task = asyncio.create_task(simulate_traffic(fake_users))

    while True:
        print("help")
        current_time = asyncio.get_event_loop().time()
        print("help2")
        if current_time >= end_time:
            # Stop the simulation after 3 minutes
            simulation_task.cancel()
            print("Stopping simulation after 3 minutes.")
            break

        # Continue running the simulation and check periodically
        await asyncio.sleep(10)

    try:
        await simulation_task
    except asyncio.CancelledError:
        print("Simulation tasks were cancelled.")

if __name__ == "__main__":
    print("ran")
    asyncio.run(main())