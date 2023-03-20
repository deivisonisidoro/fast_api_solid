# Administrator Entity

::: src.entities.administrator_entity

## Administrator Entity Diagram

```mermaid
    classDiagram
        class Administrator {
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
        Administrator --|> User
```

The above diagram represents the relationship between the `Administrator` and `User` entities. It shows that the `Administrator` entity has a one-to-one relationship with the `User` entity.
