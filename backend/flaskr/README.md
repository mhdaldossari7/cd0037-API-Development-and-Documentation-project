# API Documentation

`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category.
- Request Aurgument: `page` - integer.
- Returns: An object with 10 paginated questions, total questions, object including all categories.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 7,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 8,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 9,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 10,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": "4",
      "difficulty": 2,
      "id": 11,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 12,
      "question": "What is the largest lake in Africa?"
    }
  ],
  "success": true,
  "total_questions": 6
}
```

---

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Request Arguments: None.
- Returns: An object with a single key, categories that contain an object of id: cate_string key:value pairs.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

---

`GET '/categories/${id}/questions'`

- Fetches questions for a category specified by id request argument.
- Request Arguments: `id` - integer.
- Returns: An object with questions for the specified category, total questions, and current category.

```json
{
  "current_category": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 12,
      "question": "What is the largest lake in Africa?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

---

`DELETE '/questions/${id}'`

- Deletes a specified question using the id.
- Request Arguments: `id` - integer.
- Returns: success message, and deleted key set to true indicates the deletion is done.

```json
{
  "success": true,
  "deleted": true
}
```

---

`POST '/play'`

- Sends a post request to get the next question.
- Request Body :

```json
{
  "previous_questions": [3, 6],
  "quizz_category": "current_category"
}
```

- Returns: New questions object.

```json
{
  "question": {
    "id": 1,
    "question": "What is your name?",
    "answer": "Mohammed",
    "difficulty": 4,
    "category": 4
  }
}
```

`POST '/search'`

- Sends a post reuqest to search for a specific question.
- Request body:

```json
{
  "searchTerm": "what"
}
```

- Returns: An array of questions, a number of total questions that met the search term.

```json
{
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 7,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 8,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 12,
      "question": "What is the largest lake in Africa?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

---

`POST '/questions'`

- Send a post request to create a new question.
- Request body:

```json
{
  "questions": "What is your name?",
  "answer": "Mohammed",
  "difficulty": 4,
  "category": 2
}
```

- Returns: The newly created question id, list of questions and total number of current questions.

```json
{
  "question_id": 4,
  "questions": [
    {
      "answer": "Mohammed",
      "category": 3,
      "difficulty": 5,
      "id": 3,
      "question": "What is your name ?"
    },
    {
      "answer": "26",
      "category": 4,
      "difficulty": 3,
      "id": 5,
      "question": "How old are you ?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```
