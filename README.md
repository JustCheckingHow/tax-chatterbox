# Tax Chatter Readme

## Technology stack

Key points of the solution:

- The user can upload the document of the deal and the PCC form will be derived from it
- The user can simply describe their situation
- The system automatically asks for missing data from the document or the user description
- The user verify if the parsed data is correct.

### Deployment

- Coolify CI/CD for continuous deployment

### Frontend

- React
- Typescript

# Backend

- docker-compose
- django over ws for chat communcation

# AI

- GPT Chat 4o -- for basic text usage and chat
- Qwen v2 VL -- for pdf OCR parsing and Q&A for user-uploaded documents
