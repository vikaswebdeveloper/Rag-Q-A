import argparse
import sys
from pathlib import Path

BackendDir = Path(__file__).resolve().parent
sys.path.insert(0, str(BackendDir.parent))
sys.path.insert(0, str(BackendDir))

from backend.app.databases import UsersSession, createTables
from backend.app.models import User


def main():
    parser = argparse.ArgumentParser(description="Manage admin status for RAG Q&A users")
    parser.add_argument("email", nargs="?", help="Email of user to promote or demote")
    parser.add_argument("--remove", action="store_true", help="Remove admin rights")
    parser.add_argument("--list", action="store_true", help="List all current admins")

    args = parser.parse_args()

    # Ensure tables are created and migrated
    createTables()

    with UsersSession() as db:
        if args.list:
            admins = db.query(User).filter(User.is_admin.is_(True)).order_by(User.email).all()
            print(f"Current admins ({len(admins)}):")
            for a in admins:
                status = "verified" if a.email_verified_at else "unverified"
                print(f"  • {a.email} ({a.name}) [{status}]")
            return

        if not args.email:
            parser.print_help()
            sys.exit(1)

        email = args.email.lower().strip()
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"Error: User with email '{email}' not found.")
            sys.exit(1)

        if args.remove:
            user.is_admin = False
            db.commit()
            print(f"Success: Admin rights removed from '{email}'.")
        else:
            user.is_admin = True
            db.commit()
            print(f"Success: Admin rights granted to '{email}'.")


if __name__ == "__main__":
    main()

