## USER-PROFILE APIs

#### Registration
- `POST` /user-services/profile/registration/
```typescript
body: {
    username: string
    password: string
    password_confirm: string
    email?: string
    last_name?: string
    first_name?: string
    gender?: 'MALE' | 'FEMALE' | 'OTHER' (default)
    country?: 'VN' (default) | 'US' | ...
    city?: string
    avatar?: File
    phone?: string (ex: +84389475654)
}
```

#### Profile Apis
- `GET` /user-services/profile/:id
    ```typescript
    response: {
        pageable: null
        status_code: number
        data: {
            gender: string
            country: string
            city: string
            avatar: string
            id: string
            username: string
            first_name: string
            last_name: string
            email: string
            dob: any
            phone: string
            total_followers: number
            fullname: string
        }
    }
    ```