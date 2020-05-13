Get all users

GET /api/users/

response:
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Austin",
            "age": 19,
            "bio": "",
            "communities": [ <SERIALIZED COMMUNITY>, ... ]
        },
        {
            "id": 2,
            "name": "Trey",
            "age": 19,
            "bio": "Austin's roommate",
            "communities": [ <SERIALIZED COMMUNITY>, ... ]
        }
        ...
    ]
}
```

Note: Matches aren't retrieved in this case because I wanted to make that
information private.
________________________________________________________________________________

Create a user

POST /api/users/

request:
```json
{
    "name": <USER INPUT>,
    "age": <USER INPUT>,
    "bio": <USER INPUT>
}
```

response:
```json
{
    "success": true,
    "data": {
        "id": 1,
        "name": "Austin",
        "age": 19,
        "bio": "",
        "matches": [],
        "communities": []
    }
}
```
________________________________________________________________________________

Get a user by ID

GET /api/users/{id}/

response:
```json
{
    "success": true,
    "data": {
        "id": <ID>,
        "name": <USER INPUT FOR NAME>,
        "age": <USER INPUT FOR AGE>,
        "bio": <USER INPUT FOR BIO>,
        "matches": [ <SERIALIZED MATCH> ... ],
        "communities": [ <SERIALIZED COMMUNITY>, ... ]
    }
}
```

Note: In this case only matches where mutual interest has been shown will be
returned in the response.
________________________________________________________________________________

Delete a user by ID

DELETE /api/users/{id}/

response:
```json
{
    "success": true,
    "data": {
        "id": <ID>,
        "name": <USER INPUT FOR NAME>,
        "age": <USER INPUT FOR AGE>,
        "bio": <USER INPUT FOR BIO>,
        "matches": [ <SERIALIZED MATCH> ... ],
        "communities": [ <SERIALIZED COMMUNITY>, ... ]
    }
}
```

Note: In this case, like GET /api/users/, all matches are returned in the
response, not just ones with mutual interest.
________________________________________________________________________________

Browse through potential matches

GET /api/users/{id}/browse/

response:
```json
{
    "success": true,
    "data": {
        "id": 3,
        "name": "Jackie",
        "age": 19,
        "bio": ""
    }
}
```

Note: I wrote the backend so that when someone goes to browse potential matches:  
    &nbsp;&nbsp;&nbsp;- they won't see anyone they've seen on browse before  
    &nbsp;&nbsp;&nbsp;- if personA has seen personB on browse and did not "swipe right" then
    personA will not show up when personB is browsing potential matches
________________________________________________________________________________

Create a match

POST /api/users/{id}/browse/

request:
```json
{
    "user2_id": <USER INPUT>,
    "accepted": <USER INPUT>
}
```

response:
```json
{
    "success": true,
    "data": {
        "data": {
        "id": 9,
        "accepted": true,
        "user1_id": 5,
        "user2_id": 3
    }
    }
}
```

Note: user2_id is the ID of the person the user who is browsing wants to "swipe"
on. "Accepted" is a boolean value. There are a few possibilities based on the
value of "accepted" in the response:  
    &nbsp;&nbsp;&nbsp;-If "accepted" is set to False and the match already exists in the Match table  
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-The match's column for accepted is set to false  
    &nbsp;&nbsp;&nbsp;-If "accepted" is set to False and the match does not exist in the table  
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-A new match is created and its accepted column is false  
    &nbsp;&nbsp;&nbsp;-If "accepted" is set to True and the match is not in the table  
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-A new match is created with its accepted column set to null  
    &nbsp;&nbsp;&nbsp;-If "accepted" is set to True and the match is in the table  
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-The match's accepted column is updated from null to true
________________________________________________________________________________

Get matches for user by ID

GET /api/users/{id}/matches/

response:
```json
{
    "success": true,
    "data": [ <SERIALIZED MATCH>, ... ]
}
```

Note: Only matches where mutual interest has been shown will be returned.
________________________________________________________________________________

Get all communities

GET /api/communities/

response:
```json
{
    "success": true,
    "data": [
        {
            "name": "Project Team",
            "description": "A community for people who are on project teams",
            "members": [ <SERIALIZED USER>, ... ]
        },
        ...
    ]
}
```

Note: Members are serialized without the communities they are a member of.
________________________________________________________________________________

Join a community

POST /api/users/{user_id}/communities/{community_id}/

request: n/a

response:
```json
{
    "success": true,
    "data": {
        {
        "id": 4,
        "name": "Trey",
        "age": 19,
        "bio": "no bio",
        "matches": [],
        "communities": [
            {
                "id": 1,
                "name": "Project Teams",
                "description": "A community for members of project teams"
            }
        ]
    }
    }
}
```

Note: The communites are serialized without members.
________________________________________________________________________________

Browse potential matches by community

GET /api/users/{user_id}/browse/{community_id}/

response:
```json
{
    "success": true,
    "data": {
        "id": 4,
        "name": "Trey",
        "age": 19,
        "bio": "no bio"
    }
}
```

Note: This works the same way as the other browse route except it only filters through
the members of the specified community.
________________________________________________________________________________

Create a match with someone from a specific community

POST /api/users/{user_id}/browse/{community_id}/

request:
```json
{
    "user2_id": <USER INPUT>,
    "accepted": <USER INPUT>
}

response:
{
    "success": true,
    "data": {
        "data": {
        "id": 9,
        "accepted": true,
        "user1_id": 5,
        "user2_id": 3
    }
    }
}
```

Note: this works exactly the same as the match route above but between members of the same community.
