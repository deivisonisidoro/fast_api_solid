# Students Entity

::: src.entities.students_entity

## Students Entity Diagram

```mermaid
    classDiagram
        class Students {
            +id: int
            +user_id: int
            +user: User
            +created_at: datetime
            +updated_at: datetime
        }
        class User {
            +id: int
            +name: str
            +email: str
            +password: str
            +created_at: datetime
            +updated_at: datetime
        }
        Students --|> User
```

The above diagram represents the relationship between the `Students` and `User` entities. It shows that the `Students` entity has a one-to-one relationship with the `User` entity.
