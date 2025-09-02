#!/usr/bin/env python3
"""
Script test kết nối Firebase và đồng bộ dữ liệu
"""

from app import create_app
from models import db, User, Assessment, Contact
from firebase_config import firebase_manager
from datetime import datetime

def main():
    """Main function"""
    print("🔥 HealthFirst Firebase Test")
    print("=" * 50)
    
    # Create app context
    app = create_app()
    
    with app.app_context():
        # Test Firebase connection
        print("1. Testing Firebase connection...")
        if firebase_manager.initialized:
            print("✅ Firebase connected successfully!")
        else:
            print("❌ Firebase connection failed!")
            return
        
        # Test sync user data
        print("\n2. Testing user sync...")
        users = User.query.all()
        for user in users:
            success = firebase_manager.sync_user_to_firebase(user)
            if success:
                print(f"✅ Synced user: {user.email}")
            else:
                print(f"❌ Failed to sync user: {user.email}")
        
        # Test sync assessment data
        print("\n3. Testing assessment sync...")
        assessments = Assessment.query.all()
        for assessment in assessments:
            success = firebase_manager.sync_assessment_to_firebase(assessment)
            if success:
                print(f"✅ Synced assessment: {assessment.id}")
            else:
                print(f"❌ Failed to sync assessment: {assessment.id}")
        
        # Test sync contact data
        print("\n4. Testing contact sync...")
        contacts = Contact.query.all()
        for contact in contacts:
            success = firebase_manager.sync_contact_to_firebase(contact)
            if success:
                print(f"✅ Synced contact: {contact.id}")
            else:
                print(f"❌ Failed to sync contact: {contact.id}")
        
        # Test Firebase stats
        print("\n5. Testing Firebase statistics...")
        stats = firebase_manager.get_firebase_stats()
        if stats:
            print("✅ Firebase statistics:")
            print(f"   - Total users: {stats.get('total_users', 0)}")
            print(f"   - Total assessments: {stats.get('total_assessments', 0)}")
            print(f"   - Total contacts: {stats.get('total_contacts', 0)}")
        else:
            print("❌ Failed to get Firebase statistics")
        
        # Test creating new data
        print("\n6. Testing new data creation...")
        
        # Create test contact
        test_contact = Contact(
            name="Test User",
            email="test@example.com",
            subject="Firebase Test",
            message="This is a test message for Firebase sync",
            status="new"
        )
        
        db.session.add(test_contact)
        db.session.commit()
        
        # Sync to Firebase
        success = firebase_manager.sync_contact_to_firebase(test_contact)
        if success:
            print("✅ Created and synced test contact")
        else:
            print("❌ Failed to sync test contact")
        
        # Clean up test data
        db.session.delete(test_contact)
        db.session.commit()
        print("✅ Cleaned up test data")
    
    print("\n" + "=" * 50)
    print("🎯 Firebase test completed!")
    print("\n💡 Next steps:")
    print("   1. Run the application: python run.py")
    print("   2. Login with admin: admin@healthfirst.com / admin123")
    print("   3. Access admin dashboard: http://localhost:5000/admin")
    print("   4. Check Firebase Console for synced data")

if __name__ == '__main__':
    main()
