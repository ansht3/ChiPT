# ChiPT Core Features & Security Flow Updates

This document summarizes the changes made to the ChiPT repository to support multi-tenancy, email verification, enhanced instructor/TA workflows, and granular class role permissions.

## Backend & Database Architecture

1. **Database Multi-tenancy Models**
   - Transformed simple `UserRole` enums to `GlobalRole` (System level) and `ClassRole` (Class specific).
   - Created full `Class`, `Enrollment`, `TAAllowlist`, and `AuditLog` SQLAlchemy models to support isolated spaces and detailed tracing.
   - Upgraded `User` tables to include verification hashes, token versions, and an "intent to be an instructor" flag.

2. **Expanded Class Role Tiers (Owner, Instructor, TA, Student)**
   - Added the **`owner`** tier to `ClassRole`. When a user creates a class, they are minted as the `owner`. Only an `owner` (or global `admin`) has authorization to delete the class layout or promote/demote other `instructor` roles.
   - Upgraded the **`ta`** tier. TAs now operate with `isStaff` permissions locally. They can view the instructor-side Q&A queues, reply to students directly, and trigger the AI "Suggest Answer" tools.
   - Enforced database constraints dynamically verifying these specific tiered credentials before releasing `/instructor/...` backend queries.

3. **Email Verification Pipeline & Toggles**
   - New `project/email_utils.py` handles parsing token UUIDs.
   - Verified users can navigate the platform; unverified users are blocked via the `require_verified_user()` dependency.
   - **Environment Toggle**: Added a `.env` / `config.py` parameter `REQUIRE_EMAIL_VERIFICATION`. Setting this to `False` gracefully bypasses the email hold for all users globally, both on the backend (`/api/login`) and frontend login states.

4. **Instructor Verification Logic**
   - When a user applies with an `"intent": "instructor"` flag at registration time, they operate as a normal student until explicitly approved.
   - Token Invalidation: `auth.jwt` tokens embed `token_version`. Bumping this version immediately logs out older, expired sessions over FastAPI middleware.

5. **Class Management & Registration**
   - Implemented `POST /api/classes` and `/api/classes/{id}/rotate-code` to issue and hash randomized alphanumeric tokens (ex: `APE8ZROO`).
   - `POST /api/classes/join` allows Student users to query the platform using a verified Join Code (transactionally protected).
   - If a Student's email is located inside the pre-defined `TAAllowlist` database table upon join, the API automatically triggers an `AuditLog` action and promotes them dynamically from Student to TA!

6. **Email Address Updating**
   - Profile management endpoint (`POST /api/account/update-email`) restricts changes to authorized passwords, guarantees `@purdue.edu` formatting, resets `email_verified=False` (if required), and actively kicks all concurrent user sessions by elevating their global `token_version`.

## Interactive Admin Scripts
A suite of terminal-based administrative Python scripts was created inside `/project/` to handle sensitive database mutations safely outside the web container:
- **`change_user_role.py`**: An interactive wizard plotting out all classes and allowing an admin to alter Global Roles (e.g. promoting `students` to system `instructors`) or Class Roles (tuning `ta` vs `owner` permissions on the fly).
- **`approve_instructor.py`**: Locates pending instructor registrations and forces global approval.
- **`remove_account.py`**: Hard-deletes a user and their dependencies directly from SQLAlchemy.
- **`reset_account_password.py`**: Re-hashes and overrides account access.

## Frontend UI & Roster Refinements
- **Roster Management**: The Roster Modal (`GET /api/classes/{id}/roster`) now dynamically renders the active class Join Code. It includes **live search filtering** (by Name or Email) and **click-to-sort headers** (alphabetical, descending/ascending) computed in `app.js`.
- **Clean Dashboarding**: Users with 0 active class enrollments are smoothly redirected directly into the `Account Settings` view, hiding the Q&A panel until they successfully join a classroom.
- **Responsive Nav**: The UI cleanly handles the `owner`, `instructor`, `ta`, and `student` visual states, conditionally hiding buttons that are unauthorized (deletions, role drops) preventing false 403 blocks.

## Automated Verification
Tests in `tests/test_auth_flows.py` and `tests/test_class_flows.py` utilize `sqlite+aiosqlite:///:memory:` to isolate regressions. They prove backend routes accurately execute 403 Forbidden catches for students poking at instructor spaces and accurately validate dynamic token rotations.
