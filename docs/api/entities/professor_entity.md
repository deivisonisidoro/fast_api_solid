# Professor Entity

::: src.entities.professor_entity

## Professor Entity Diagram

```mermaid
    classDiagram
        class Professor {
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
        Professor --|> User
```

The above diagram represents the relationship between the `Professor` and `User` entities. It shows that the `Professor` entity has a one-to-one relationship with the `User` entity.
