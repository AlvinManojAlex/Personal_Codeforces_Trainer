import requests

def get_accepted_problems(username):
    url = f"https://codeforces.com/api/user.status?handle={username}&from=1&count=10000"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if data['status'] == 'OK':
            accepted_problems = set()

            for submission in data['result']:
                if submission['verdict'] == 'OK':
                    problem = submission['problem']
                    problem_code = f"{problem['contestId']}{problem['index']}"
                    accepted_problems.add(problem_code)
            return accepted_problems
        
    return None

def generate_problems(username, ratings, num_problems):
    generated_problems = []
    accepted_problems = get_accepted_problems(username)

    for rating in ratings:
        problems_for_rating = []
        url = f"https://codeforces.com/api/problemset.problems?rating={rating}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            # print(data)

            if data['status'] == 'OK':
                problems = data['result']['problems']
                # print(problems[:100])

                for problem in problems:
                    if 'rating' in problem:  # Check if the problem has a rating associated with it
                        problem_code = f"{problem['contestId']}{problem['index']}"

                        if problem_code not in accepted_problems:  # Exclude already solved problems
                            problems_for_rating.append(problem_code)

                if problems_for_rating:
                    generated_problems.extend(problems_for_rating[:min(num_problems, len(problems_for_rating))])
                else:
                    print(f"No unsolved problems found for rating {rating}.")
            else:
                print("Failed to fetch problems. Please try again later.")
        else:
            print("Failed to fetch problems. Please try again later.")
        
    
    return generated_problems

def main():

    username = input("Enter your Codeforces username: ")
    num_problems = int(input("Enter the number of problems to generate: "))
    ratings = input("Enter the ratings of the problems: ").split()

    generated_problems = generate_problems(username, ratings, num_problems)

    print("Generated problems:")
    for problem_code in generated_problems:
        print(problem_code)

if __name__ == "__main__":
    main()