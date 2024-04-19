# API Documentation

## Register a new user

### Request
`POST /register/`

### Body
```
{
    "email": "<user email>",
    "password": "<user password>"
}
```
### Response
Returns a newly created user and a JSON Web Token (JWT) for the user to authenticate future requests.

## User login
Authenticates a user with given credentials.

### Request
`POST /user_login/`

### Parameters
- `email` (string) : User's email.
- `password` (string) : User's password.

### Response
Returns the authenticated user along with a JWT token to authenticate future requests.

## Fetch user's name

### Request
`GET /user/name/`

### Headers
- `Authorization` : `Bearer <access_token>`

### Response
Returns the username of the authenticated user.

## Fetch user's pending and Upcoming Events

Fetches events associated with the authenticated user's email.

### Request
`GET /user_events/`

### Headers
- `Authorization` : `Bearer <access_token>`

### Response
Returns a list of events (pending and upcoming) associated with the authenticated user.

## Fetch event details by event ID

Fetches details of a specific event by event id.

### Request
`GET /events/{event_id}`

### Path parameters
- `event_id` (integer) : ID of the event to retrieve.

### Response
Returns the details of the event with the given ID. If no such event exists, returns `404 Not Found`.

---
Note: In the Headers section, `<access_token>` must be replaced with the actual access token received upon registration or login.

The endpoints require authentication. A JWT token that is received upon registration or login needs to be included in the `Authorization` header of future requests.

To include the token, add `Authorization: Bearer <access_token>` to the headers where `<access_token>` is the token you received. The `Bearer` keyword indicates that a token is being used for authorization.

Example:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```
