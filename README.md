### Challenge
[Real-Time Quiz](challenge.md)

### System Design
[Real-Time Quiz System Design](system_design/system_design.md)

### Implementation
This project is the implementation of Real-Time Score Updates Service in the real-time quiz system.

Technology stack:
- Django + Django Rest Framework

All source code is in the `src` directory. The source code is divided into the following directories:
- `core`: Contains the common code used in the service such as utils, db models
- `main`: Django settings
- `user_score`: Contains the code for the user score service including api of answer a question and its unit tests

Code flow in user_score folder:
- `apis`: Contains the api for the user score service
- `services`: Contains the business logic of the user score service
- `tests`: Contains the unit tests of the user score including the test for the api and the service

1. When an api is called, it will go to view in the `apis` directory. 
1. Data will be validated in the serializer
1. Then the validated data will be passed to the service in the `services` directory
1. The service will process the data and return the result to the view
1. While processing the answer of the participant, it uses lock to prevent multiple requests to update the score of the same user
1. The view will return the result to the client
1. The unit tests are in the `tests` directory and run by the command `pytest`

### What is implemented
- User can answer a question
- After answering a question, the user score in the quiz will be updated
- The user can only answer the question once
- Once database was updated, system will send a message to the message broker to notify Real-Time leaderboard service to update the user score in the quiz
- Add sentry for error tracking
- Add new relic for performance and log monitoring
- Add swagger for API documentation

### How to run
1. Build docker image
```bash
docker build -t user_score_service .
```
1. Set environment variables in the `.env` file
```
Follow the syntax in the .env.example file
```

1. Run docker container
```bash
docker run -p 8000:8000 user_score_service
```

### How to test
1. Run the command
```bash
docker exec -it <container_id> pytest
```

### API documentation
Swagger
```
http://localhost:8000/quiz-api-doc
```