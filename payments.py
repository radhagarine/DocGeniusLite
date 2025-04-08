import os
import stripe
import uuid
from db import get_db_connection

# Initialize Stripe with the API key from environment variables
stripe.api_key = os.getenv("STRIPE_API_KEY", "sk_test_example")

def process_payment(user_id, token, amount, document_id):
    """Process a one-time payment for a document"""
    try:
        # Create a charge using Stripe
        charge = stripe.Charge.create(
            amount=int(amount * 100),  # Convert to cents
            currency="usd",
            source=token,
            description=f"Document purchase for user {user_id}"
        )
        
        # Record the payment in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        payment_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO payments 
            (id, user_id, amount, currency, payment_type, document_id, status, stripe_payment_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                payment_id,
                user_id,
                amount,
                "USD",
                "document",
                document_id,
                "completed",
                charge.id
            )
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return payment_id
    
    except stripe.error.StripeError as e:
        # Log the error and update the payment status in the database
        print(f"Stripe error: {str(e)}")
        
        # Record the failed payment
        conn = get_db_connection()
        cursor = conn.cursor()
        
        payment_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO payments 
            (id, user_id, amount, currency, payment_type, document_id, status, stripe_payment_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                payment_id,
                user_id,
                amount,
                "USD",
                "document",
                document_id,
                "failed",
                None
            )
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        raise Exception(f"Payment failed: {str(e)}")

def create_subscription(user_id, token, plan):
    """Create a subscription for a user"""
    try:
        # Create a customer in Stripe
        customer = stripe.Customer.create(
            source=token,
            description=f"Customer for user {user_id}"
        )
        
        # Create a subscription for the customer
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{"plan": "pro_monthly"}],  # This would be your actual plan ID in Stripe
            expand=["latest_invoice.payment_intent"]
        )
        
        # Record the subscription payment
        conn = get_db_connection()
        cursor = conn.cursor()
        
        payment_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO payments 
            (id, user_id, amount, currency, payment_type, status, stripe_payment_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                payment_id,
                user_id,
                9.00,  # $9/month for Pro plan
                "USD",
                "subscription",
                "completed",
                subscription.id
            )
        )
        
        # Update user's subscription status
        cursor.execute(
            "UPDATE users SET subscription = %s WHERE id = %s",
            (plan, user_id)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return subscription.id
    
    except stripe.error.StripeError as e:
        # Log the error
        print(f"Stripe error: {str(e)}")
        raise Exception(f"Subscription creation failed: {str(e)}")

def check_user_can_create_document(user_id):
    """Check if a user can create more documents based on their subscription/usage"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user's subscription status
    cursor.execute("SELECT subscription FROM users WHERE id = %s", (user_id,))
    subscription = cursor.fetchone()[0]
    
    # If Pro, they have unlimited documents
    if subscription == "pro":
        cursor.close()
        conn.close()
        return True, None
    
    # For free users, check their document count this month
    current_month = datetime.datetime.now().strftime('%Y-%m')
    cursor.execute(
        """
        SELECT COUNT(*) FROM documents 
        WHERE user_id = %s AND created_at >= %s::date
        """, 
        (user_id, f"{current_month}-01")
    )
    doc_count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    # Free users get 3 documents per month
    if doc_count < 3:
        return True, None
    else:
        return False, "You've reached your free document limit for this month. Purchase this document or upgrade to Pro for unlimited documents."

import datetime
