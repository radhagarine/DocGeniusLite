# Invoice Template

import datetime

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
    """
    Generate an Invoice document based on the provided parameters
    
    Args:
        parameters: A dictionary containing all the parameter values
        
    Returns:
        HTML content for the document
    """
    # Format dates
    invoice_date = parameters.get("invoice_date", "")
    if isinstance(invoice_date, str):
        formatted_invoice_date = invoice_date
    else:
        formatted_invoice_date = invoice_date.strftime("%B %d, %Y") if invoice_date else ""
    
    due_date = parameters.get("due_date", "")
    if isinstance(due_date, str):
        formatted_due_date = due_date
    else:
        formatted_due_date = due_date.strftime("%B %d, %Y") if due_date else ""
    
    # Get parameters with defaults
    business_name = parameters.get("business_name", "[BUSINESS NAME]")
    business_address = parameters.get("business_address", "[BUSINESS ADDRESS]")
    business_phone = parameters.get("business_phone", "[PHONE]")
    business_email = parameters.get("business_email", "[EMAIL]")
    
    client_name = parameters.get("client_name", "[CLIENT NAME]")
    client_address = parameters.get("client_address", "[CLIENT ADDRESS]")
    client_email = parameters.get("client_email", "")
    client_phone = parameters.get("client_phone", "")
    
    invoice_number = parameters.get("invoice_number", "[INVOICE #]")
    payment_terms = parameters.get("payment_terms", "Net 30")
    currency = parameters.get("currency", "USD")
    
    line_items_text = parameters.get("line_items", "")
    tax_rate = float(parameters.get("tax_rate", 0))
    shipping = float(parameters.get("shipping", 0))
    
    notes = parameters.get("notes", "")
    payment_instructions = parameters.get("payment_instructions", "")
    
    # Process line items
    line_items = []
    subtotal = 0
    
    for line in line_items_text.split('\n'):
        if not line.strip():
            continue
            
        parts = [part.strip() for part in line.split('|')]
        if len(parts) >= 3:
            description = parts[0]
            try:
                quantity = float(parts[1])
                unit_price = float(parts[2])
                line_total = quantity * unit_price
                subtotal += line_total
                
                line_items.append({
                    "description": description,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "line_total": line_total
                })
            except ValueError:
                # Handle invalid number format
                line_items.append({
                    "description": description,
                    "quantity": parts[1],
                    "unit_price": parts[2],
                    "line_total": 0
                })
        elif len(parts) == 1 and parts[0]:
            # Just a description
            line_items.append({
                "description": parts[0],
                "quantity": "",
                "unit_price": "",
                "line_total": 0
            })
    
    # Calculate totals
    tax_amount = subtotal * (tax_rate / 100)
    total = subtotal + tax_amount + shipping
    
    # Currency symbol mapping
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "CAD": "C$",
        "AUD": "A$"
    }
    currency_symbol = currency_symbols.get(currency, currency)
    
    # Generate the document content
    document = f"""
    <div style="font-family: Arial, sans-serif;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 30px;">
            <div>
                <h1 style="color: #2E86C1;">INVOICE</h1>
                <div style="margin-top: 20px;">
                    <p><strong>{business_name}</strong></p>
                    <p>{business_address.replace('\n', '<br>')}</p>
                    <p>Phone: {business_phone}</p>
                    <p>Email: {business_email}</p>
                </div>
            </div>
            <div style="text-align: right;">
                <h2>Invoice #{invoice_number}</h2>
                <p><strong>Date:</strong> {formatted_invoice_date}</p>
                <p><strong>Due Date:</strong> {formatted_due_date}</p>
                <p><strong>Terms:</strong> {payment_terms}</p>
            </div>
        </div>
        
        <div style="margin-bottom: 30px;">
            <h3 style="border-bottom: 1px solid #ccc; padding-bottom: 5px;">Bill To:</h3>
            <p><strong>{client_name}</strong></p>
            <p>{client_address.replace('\n', '<br>')}</p>
            {f"<p>Phone: {client_phone}</p>" if client_phone else ""}
            {f"<p>Email: {client_email}</p>" if client_email else ""}
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
            <tbody>
    """
    
    # Add line items
    for item in line_items:
        document += f"""
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{item['description']}</td>
                    <td style="padding: 10px; text-align: right; border-bottom: 1px solid #ddd;">{item['quantity']}</td>
                    <td style="padding: 10px; text-align: right; border-bottom: 1px solid #ddd;">{currency_symbol}{item['unit_price']:.2f}</td>
                    <td style="padding: 10px; text-align: right; border-bottom: 1px solid #ddd;">{currency_symbol}{item['line_total']:.2f}</td>
                </tr>
        """
    
    # Add totals
    document += f"""
            </tbody>
        </table>
        
        <div style="display: flex; justify-content: flex-end;">
            <div style="width: 300px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <div>Subtotal:</div>
                    <div>{currency_symbol}{subtotal:.2f}</div>
                </div>
    """
    
    if tax_rate > 0:
        document += f"""
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <div>Tax ({tax_rate}%):</div>
                    <div>{currency_symbol}{tax_amount:.2f}</div>
                </div>
        """
    
    if shipping > 0:
        document += f"""
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <div>Shipping/Handling:</div>
                    <div>{currency_symbol}{shipping:.2f}</div>
                </div>
        """
    
    document += f"""
                <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 1.2em; margin-top: 10px; padding-top: 10px; border-top: 2px solid #ddd;">
                    <div>Total:</div>
                    <div>{currency_symbol}{total:.2f} {currency}</div>
                </div>
            </div>
        </div>
    """
    
    # Add notes and payment instructions
    if notes or payment_instructions:
        document += f"""
        <div style="margin-top: 30px; border-top: 1px solid #ddd; padding-top: 20px;">
        """
        
        if notes:
            document += f"""
            <div style="margin-bottom: 20px;">
                <h3>Notes:</h3>
                <p>{notes.replace('\n', '<br>')}</p>
            </div>
            """
        
        if payment_instructions:
            document += f"""
            <div>
                <h3>Payment Instructions:</h3>
                <p>{payment_instructions.replace('\n', '<br>')}</p>
            </div>
            """
        
        document += """
        </div>
        """
    
    # Add footer
    document += f"""
        <div style="margin-top: 30px; text-align: center; color: #777; font-size: 0.9em;">
            <p>Thank you for your business!</p>
        </div>
    </div>
    """
    
    return document
