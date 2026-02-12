# Contact Us API Endpoint

## Overview
The Contact Us API endpoint allows users to submit inquiries that will be sent via email to the admin.

## Endpoint
```
POST /contact/
```

## Request Format
The endpoint expects a JSON payload with the following fields:

- `name` (string, required): The name of the person submitting the form
- `whatsapp_number` (string, optional): The WhatsApp number of the person
- `about` (string, optional): Information about the person or company
- `email` (string, required): The email address of the person
- `subject` (string, required): The subject of the inquiry
- `message` (string, required): The detailed message

### Example Request
```json
{
  "name": "John Doe",
  "whatsapp_number": "+1234567890",
  "about": "Potential customer interested in services",
  "email": "john@example.com",
  "subject": "Service Inquiry",
  "message": "I am interested in learning more about your transfer services."
}
```

## Response
On successful submission, the API returns:
```json
{
  "message": "Contact form submitted successfully"
}
```

Status code: `200 OK`

## Error Responses
- `400 Bad Request`: If required fields are missing or invalid JSON is provided
- `500 Internal Server Error`: If there's an issue sending the email

### Example Error Response
```json
{
  "error": "Name is required"
}
```

## Email Configuration
The contact form submission is sent via email using the `EMAIL_FROM` setting from Django settings. The email is sent to the same address configured as the `EMAIL_FROM`.

## Additional Notes
- The endpoint is CSRF exempt to allow cross-origin requests
- All email validations happen on the server side
- The email body includes all submitted fields for comprehensive information