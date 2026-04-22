# Database Architecture

## Tables

### channels
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key, generated in Python |
| name | varchar | Channel name |
| username | varchar | Channel username |
| description | text | Channel description |
| followers_count | int | Number of subscribers |
| avatar_url | varchar | Link to channel avatar |
| created_at | timestamp | When we parsed the channel |

### posts
| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key, generated in Python |
| channel_id | uuid | Foreign key → channels.id |
| message_id | int | Original Telegram message ID |
| text | text | Post content |
| published_at | timestamp | Publication date |
| views_count | int | Number of views |
| comments_count | int | Number of comments |
| replies_count | int | Number of replies |
| reposts_count | int | Number of reposts |

## Indexes

- `UNIQUE (channel_id, message_id)` — prevents duplicates and speeds up lookups