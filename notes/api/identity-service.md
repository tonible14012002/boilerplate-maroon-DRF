


## AUTH APIs
#### Login
- `post` /identity-services/token/
    ```typescript
    body: {
        username: string,
        password: string
    }
    ```
    ```typescript
    response: {
        pageable: null
        data: {
            user: {...}
            access: string
            refresh: string
        }
    }
    ```

- `post` /identity-services/refresh/
    ```typescript
    body: {
        refresh: string
    }
    ```

- `post` /identity-services/profile 
    ```typescript
    headers: {
        `AuthorizationHeader`: string
    }
    ```
    ```typescript
    response: {
        pageable: null
        data: {...} // user profile data
    }
    ```