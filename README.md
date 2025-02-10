# dzeencode-test-task


This project is a Fast API for receiving weather.

## Features
- **Dockerized**:
  - Simplified deployment using Docker.
- **API Documentation**:
  - Integrated Swagger documentation.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Docker (for containerized setup)

### Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/SysoevDmitro/keymakr-test.git
   cd keymakr-test
   ```
2. **Create a Virtual Environment:**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```
4. **Run with Docker:**
   ```
   docker-compose up --build
   ```
5. **Go to Website**
   ```
   http://127.0.0.1:8000/docs
   ```
  Here you can test API
### Documentation
- Go to `/doc` to test api
- at `/tasks/{task_id}` you will receive link to weather data
=======

