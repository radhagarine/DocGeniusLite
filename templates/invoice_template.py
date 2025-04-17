# Invoice Template

import datetime
import os

# Define the parameter structure for this document type
PARAMETERS = [
    {
        "section": "Business Information",
        "fields": [
            {
                "id": "business_name",
                "label": "Business Name",
                "type": "text",
                "required": True,
                "help": "Your business or company name"
            },
            {
                "id": "business_address",
                "label": "Business Address",
                "type": "textarea",
                "required": True,
                "help": "Your complete business address"
            },
            {
                "id": "business_phone",
                "label": "Business Phone",
                "type": "text",
                "required": True,
                "help": "Your business phone number"
            },
            {
                "id": "business_email",
                "label": "Business Email",
                "type": "text",
                "required": True,
                "help": "Your business email address"
            }
        ]
    },
    {
        "section": "Client Information",
        "fields": [
            {
                "id": "client_name",
                "label": "Client Name",
                "type": "text",
                "required": True,
                "help": "Client's full name or company name"
            },
            {
                "id": "client_address",
                "label": "Client Address",
                "type": "textarea",
                "required": True,
                "help": "Client's complete address"
            },
            {
                "id": "client_email",
                "label": "Client Email",
                "type": "text",
                "required": False,
                "help": "Client's email address"
            },
            {
                "id": "client_phone",
                "label": "Client Phone",
                "type": "text",
                "required": False,
                "help": "Client's phone number"
            }
        ]
    },
    {
        "section": "Invoice Details",
        "fields": [
            {
                "id": "invoice_number",
                "label": "Invoice Number",
                "type": "text",
                "required": True,
                "help": "A unique identifier for this invoice (e.g., INV-2023-001)"
            },
            {
                "id": "invoice_date",
                "label": "Invoice Date",
                "type": "date",
                "required": True,
                "help": "Date the invoice is issued"
            },
            {
                "id": "due_date",
                "label": "Due Date",
                "type": "date",
                "required": True,
                "help": "Date the payment is due"
            },
            {
                "id": "payment_terms",
                "label": "Payment Terms",
                "type": "select",
                "options": ["Due on Receipt", "Net 15", "Net 30", "Net 60", "Custom"],
                "required": True,
                "default": "Net 30",
                "help": "Terms of payment for this invoice"
            },
            {
                "id": "currency",
                "label": "Currency",
                "type": "select",
                "options": ["USD", "EUR", "GBP", "CAD", "AUD", "Other"],
                "required": True,
                "default": "USD",
                "help": "Currency for this invoice"
            }
        ]
    },
    {
        "section": "Line Items",
        "fields": [
            {
                "id": "line_items",
                "label": "Line Items (one per line in format: Description | Quantity | Unit Price)",
                "type": "textarea",
                "required": True,
                "help": "Enter each item on a new line in the format: Description | Quantity | Unit Price"
            },
            {
                "id": "tax_rate",
                "label": "Tax Rate (%)",
                "type": "number",
                "required": False,
                "default": 0,
                "help": "Tax rate as a percentage (e.g., 7.5 for 7.5%)"
            },
            {
                "id": "shipping",
                "label": "Shipping/Handling Fee",
                "type": "number",
                "required": False,
                "default": 0,
                "help": "Additional shipping or handling fees if applicable"
            }
        ]
    },
    {
        "section": "Additional Information",
        "fields": [
            {
                "id": "notes",
                "label": "Notes",
                "type": "textarea",
                "required": False,
                "help": "Any additional notes or terms to include on the invoice"
            },
            {
                "id": "payment_instructions",
                "label": "Payment Instructions",
                "type": "textarea",
                "required": False,
                "help": "Instructions for how the client should pay (e.g., bank details, payment methods accepted)"
            }
        ]
    }
]

def generate(parameters):
    # Extract parameters
    business_name = parameters.get('business_name', '')
    business_address = parameters.get('business_address', '')
    business_phone = parameters.get('business_phone', '')
    business_email = parameters.get('business_email', '')
    
    client_name = parameters.get('client_name', '')
    client_address = parameters.get('client_address', '')
    client_phone = parameters.get('client_phone', '')
    client_email = parameters.get('client_email', '')
    
    invoice_number = parameters.get('invoice_number', '')
    invoice_date = parameters.get('invoice_date', '')
    due_date = parameters.get('due_date', '')
    payment_terms = parameters.get('payment_terms', '')
    
    line_items_text = parameters.get('line_items', '')
    tax_rate = float(parameters.get('tax_rate', 0))
    shipping = float(parameters.get('shipping', 0))
    notes = parameters.get('notes', '')
    payment_instructions = parameters.get('payment_instructions', '')
    
    # Process line items
    line_items = []
    subtotal = 0
    
    for line in line_items_text.split('\n'):
        if line.strip():
            parts = [part.strip() for part in line.split('|')]
            if len(parts) == 3:
                desc, qty, price = parts
                try:
                    qty = float(qty)
                    price = float(price)
                    amount = qty * price
                    subtotal += amount
                    line_items.append({
                        'description': desc,
                        'quantity': qty,
                        'unit_price': price,
                        'amount': amount
                    })
                except ValueError:
                    continue

    # Calculate totals
    tax_amount = subtotal * (tax_rate / 100)
    total = subtotal + tax_amount + shipping

    # Check if company logo exists
    company_logo = parameters.get('company_logo', '')
    logo_html = ''
    if company_logo and os.path.exists(company_logo):
        import base64
        with open(company_logo, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{encoded_string}" style="max-height: 80px; max-width: 200px; margin-bottom: 15px;">'
    
    # Generate HTML
    document = f"""
    <div style="max-width: 800px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 40px;">
            <div>
                {logo_html}
                <h1 style="color: #2c3e50; margin: 0; font-size: 28px;">INVOICE</h1>
                <div style="margin-top: 20px;">
                    <p style="margin: 5px 0;"><strong>{business_name}</strong></p>
                    <p style="margin: 5px 0; white-space: pre-line;">{business_address}</p>
                    <p style="margin: 5px 0;">Phone: {business_phone}</p>
                    <p style="margin: 5px 0;">Email: {business_email}</p>
                </div>
            </div>
            <div style="text-align: right;">
                <h2 style="color: #7f8c8d; margin: 0;">Invoice #{invoice_number}</h2>
                <p style="margin: 5px 0;">Date: {invoice_date}</p>
                <p style="margin: 5px 0;">Due Date: {due_date}</p>
                <p style="margin: 5px 0;">Terms: {payment_terms}</p>
            </div>
        </div>

        <div style="margin-bottom: 30px;">
            <h3 style="border-bottom: 1px solid #ccc; padding-bottom: 5px;">Bill To:</h3>
            <p style="margin: 5px 0;"><strong>{client_name}</strong></p>
            <p style="margin: 5px 0; white-space: pre-line;">{client_address}</p>
            <p style="margin: 5px 0;">Phone: {client_phone}</p>
            <p style="margin: 5px 0;">Email: {client_email}</p>
        </div>

        <table style="width: 100%; border-collapse: collapse; margin-bottom: 30px;">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Description</th>
                    <th style="padding: 10px; text-align: right; border-bottom: 2px solid #ddd;">Quantity</th>
                    <th style="padding: 10px; text-align: right; border-bottom: 2px solid #ddd;">Unit Price</th>
                    <th style="padding: 10px; text-align: right; border-bottom: 2px solid #ddd;">Amount</th>
                </tr>
            </thead>
            <tbody>"""

    for item in line_items:
        document += f"""
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{item['description']}</td>
                    <td style="padding: 10px; text-align: right; border-bottom: 1px solid #ddd;">{item['quantity']}</td>
                    <td style="padding: 10px; text-align: right; border-bottom: 1px solid #ddd;">${item['unit_price']:.2f}</td>
                    <td style="padding: 10px; text-align: right; border-bottom: 1px solid #ddd;">${item['amount']:.2f}</td>
                </tr>"""

    document += f"""
            </tbody>
        </table>

        <div style="margin-left: auto; width: 300px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <strong>Subtotal:</strong>
                <span>${subtotal:.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <strong>Tax ({tax_rate}%):</strong>
                <span>${tax_amount:.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <strong>Shipping:</strong>
                <span>${shipping:.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 10px; padding-top: 10px; border-top: 2px solid #2c3e50;">
                <strong>Total:</strong>
                <span style="font-size: 1.2em; font-weight: bold;">${total:.2f}</span>
            </div>
        </div>"""

    if notes:
        document += f"""
        <div style="margin-top: 40px;">
            <h3 style="border-bottom: 1px solid #ccc; padding-bottom: 5px;">Notes:</h3>
            <p style="white-space: pre-line;">{notes}</p>
        </div>"""

    if payment_instructions:
        document += f"""
        <div style="margin-top: 20px;">
            <h3 style="border-bottom: 1px solid #ccc; padding-bottom: 5px;">Payment Instructions:</h3>
            <p style="white-space: pre-line;">{payment_instructions}</p>
        </div>"""

    document += """
        <div style="margin-top: 40px; text-align: center; color: #7f8c8d; font-size: 0.9em;">
            <p>Thank you for your business!</p>
        </div>
    </div>
    """

    return document
