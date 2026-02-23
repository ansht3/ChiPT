import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import async_session_maker, User, Enrollment, Class
from sqlalchemy import select

async def interactive_change_role():
    async with async_session_maker() as session:
        # 1. Output all classes and their IDs
        print("\n--- Available Classes ---")
        result = await session.execute(select(Class))
        classes = result.scalars().all()
        for c in classes:
            print(f"ID: {c.id:<4} | Name: {c.name}")
        print("-" * 25)
        
        # 2. Prompt for email
        email = input("\nEnter the email of the user you want to modify: ").strip()
        if not email:
            print("Email cannot be empty. Exiting.")
            return
            
        # Verify user exists
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user:
            print(f"User with email '{email}' not found. Exiting.")
            return
            
        # 3. Prompt for the role
        print("\n--- Available Roles ---")
        print("  Global roles: student, instructor, admin")
        print("  Class roles:  student, ta, instructor, owner")
        new_role = input("\nEnter the new role: ").strip().lower()
        
        valid_roles = ["student", "ta", "instructor", "admin", "owner"]
        if new_role not in valid_roles:
            print(f"Error: '{new_role}' is not a valid role. Exiting.")
            return

        # 4. Prompt for class ID (optional for global roles)
        class_input = input("\nEnter Class ID (leave blank to change GLOBAL role instead): ").strip()
        
        if class_input:
            # Change CLASS role
            try:
                class_id = int(class_input)
            except ValueError:
                print("Error: Class ID must be an integer. Exiting.")
                return
                
            if new_role not in ["student", "ta", "instructor", "owner"]:
                print(f"Error: '{new_role}' is not a valid class role. Exiting.")
                return
                
            enroll_res = await session.execute(
                select(Enrollment).where(
                    Enrollment.class_id == class_id, 
                    Enrollment.user_id == user.id
                )
            )
            enrollment = enroll_res.scalar_one_or_none()
            if not enrollment:
                print(f"User '{email}' is not enrolled in class ID {class_id}. Exiting.")
                return
            
            old_role = enrollment.class_role if isinstance(enrollment.class_role, str) else enrollment.class_role.value
            enrollment.class_role = new_role
            await session.commit()
            print(f"\n✅ Successfully changed {email}'s role in Class {class_id} from '{old_role}' to '{new_role}'.")
            
        else:
            # Change GLOBAL role
            if new_role not in ["student", "instructor", "admin"]:
                print(f"Error: '{new_role}' is not a valid global role. Exiting.")
                return
                
            old_role = user.global_role if isinstance(user.global_role, str) else user.global_role.value
            user.global_role = new_role
            if new_role in ["instructor", "admin"]:
                user.is_instructor_pending = False
            await session.commit()
            print(f"\n✅ Successfully changed {email}'s GLOBAL role from '{old_role}' to '{new_role}'.")

if __name__ == "__main__":
    try:
        asyncio.run(interactive_change_role())
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
