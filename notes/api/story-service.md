# STORY-SERVICE APIs

## Stories
- `GET` /story-services/stories/archieved
    + Get profile user's archieved stories
    ```typescript
    response: {
        pageable: {
            
        },
        data: Array<{
            id: string
            media_url: string
            live_time: number
            expired: boolean
            duration: number
            media_type: 'VIDEO' | 'IMAGE'
            privacy_mode: 'PRIVATE' | 'PUBLIC' | 'FRIEND_ONLY'
        }>
    }
    ```
- `GET` /story-services/stories/
    + Get user's stories list of friends.
    ```typescript
    response: {

    },
    data: Array<{
        user: {
            id: string
            nickname: string
            avatar: string
            fullname: string
            ...
        },
        stories: Array<{
            id: string
            live_time: number
            expired: boolean
            duration: number
            media_type: 'VIDEO' | 'IMAGE'
            privacy_mode: 'PUBLIC'
        }>
    }>
    ```