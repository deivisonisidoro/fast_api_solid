# User Types

In our system, there are three main user types: `Professor`, `Student`, and `Administrator`. Each user type has different roles and responsibilities.

## Professor

A professor can:

- Teach one or more courses
- Create and manage exams for their courses

## Student

A student can:

- Enroll in one or more courses
- View and complete assignments for their courses

## Administrator

An administrator can:

- Manage courses
- Manage users

## User Types Diagram

```mermaid
graph TD
  User((User))
  Professor((Professor))
  Student((Student))
  Admin((Administrator))

  User -->|has a| Professor
  User -->|has a| Student
  User -->|has a| Admin


  style User fill:#ffddcc,stroke:#ffa07a,stroke-width:2px
  style Professor fill:#a9e5bb,stroke:#4CAF50,stroke-width:2px
  style Student fill:#b2d8ff,stroke:#2196F3,stroke-width:2px
  style Admin fill:#f7e7cc,stroke:#FF9800,stroke-width:2px


```
