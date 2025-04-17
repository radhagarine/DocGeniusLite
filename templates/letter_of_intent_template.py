# Letter of Intent Template

# Define the parameter structure for this document type
PARAMETERS = [
    {
        "section": "Parties Information",
        "fields": [
            {
                "id": "sender_name",
                "label": "Sender Name",
                "type": "text",
                "required": True,
                "help": "Your full name or company name"
            },
            {
                "id": "sender_address",
                "label": "Sender Address",
                "type": "textarea",
                "required": True,
                "help": "Your complete address"
            },
            {
                "id": "recipient_name",
                "label": "Recipient Name",
                "type": "text",
                "required": True,
                "help": "Full name or company name of the recipient"
            },
            {
                "id": "recipient_address",
                "label": "Recipient Address",
                "type": "textarea",
                "required": True,
                "help": "Complete address of the recipient"
            }
        ]
    },
    {
        "section": "Letter Details",
        "fields": [
            {
                "id": "letter_date",
                "label": "Date",
                "type": "date",
                "required": True,
                "help": "Date of the letter"
            },
            {
                "id": "subject",
                "label": "Subject",
                "type": "text",
                "required": True,
                "help": "Subject of the letter of intent"
            },
            {
                "id": "intent_type",
                "label": "Type of Intent",
                "type": "select",
                "options": [
                    "Business Partnership", 
                    "Business Acquisition", 
                    "Joint Venture", 
                    "Service Agreement", 
                    "Real Estate Transaction", 
                    "Employment", 
                    "Other"
                ],
                "required": True,
                "help": "The type of intent being expressed"
            }
        ]
    },
    {
        "section": "Intent Details",
        "fields": [
            {
                "id": "introduction",
                "label": "Introduction",
                "type": "textarea",
                "required": True,
                "default": "This Letter of Intent (\"LOI\") sets forth the basic terms of a proposed transaction between the parties. While this LOI represents the understanding of the parties regarding the proposed transaction, it is not legally binding except as stated in the 'Binding Provisions' section.",
                "help": "Brief introduction stating the purpose of the letter"
            },
            {
                "id": "transaction_description",
                "label": "Transaction Description",
                "type": "textarea",
                "required": True,
                "help": "Detailed description of the proposed transaction or relationship"
            },
            {
                "id": "proposed_terms",
                "label": "Proposed Terms",
                "type": "textarea",
                "required": True,
                "help": "Key terms and conditions of the proposed transaction"
            },
            {
                "id": "timeline",
                "label": "Timeline",
                "type": "textarea",
                "required": True,
                "help": "Expected timeline for next steps and completion"
            }
        ]
    },
    {
        "section": "Additional Terms",
        "fields": [
            {
                "id": "confidentiality",
                "label": "Confidentiality Clause",
                "type": "textarea",
                "required": False,
                "default": "The parties agree to maintain the confidentiality of any information exchanged in connection with this LOI and the proposed transaction. This confidentiality provision shall be binding regardless of whether the parties proceed with the proposed transaction.",
                "help": "Terms related to the confidentiality of discussions"
            },
            {
                "id": "exclusivity",
                "label": "Exclusivity Period",
                "type": "textarea",
                "required": False,
                "help": "Any exclusivity provisions (if applicable)"
            },
            {
                "id": "expenses",
                "label": "Expenses",
                "type": "textarea",
                "required": False,
                "default": "Each party shall bear its own expenses related to this LOI and the proposed transaction, including but not limited to legal, accounting, and advisory fees.",
                "help": "How expenses will be handled"
            },
            {
                "id": "governing_law",
                "label": "Governing Law",
                "type": "text",
                "required": True,
                "help": "State or jurisdiction whose laws will govern this letter"
            }
        ]
    },
    {
        "section": "Closing",
        "fields": [
            {
                "id": "closing_statement",
                "label": "Closing Statement",
                "type": "textarea",
                "required": False,
                "default": "We look forward to working together toward a mutually beneficial relationship. If the terms outlined in this Letter of Intent are acceptable, please indicate your agreement by signing below.",
                "help": "Final statement before signature lines"
            },
            {
                "id": "sender_signatory",
                "label": "Sender Signatory Name",
                "type": "text",
                "required": True,
                "help": "Name of person signing on behalf of sender"
            },
            {
                "id": "sender_title",
                "label": "Sender Title",
                "type": "text",
                "required": True,
                "help": "Title of person signing on behalf of sender"
            },
            {
                "id": "recipient_signatory",
                "label": "Recipient Signatory Name",
                "type": "text",
                "required": True,
                "help": "Name of person signing on behalf of recipient"
            },
            {
                "id": "recipient_title",
                "label": "Recipient Title",
                "type": "text",
                "required": True,
                "help": "Title of person signing on behalf of recipient"
            }
        ]
    }
]

def generate(parameters):
    """Generate a letter of intent document"""
    # Extract parameters
    sender_name = parameters.get('sender_name', '')
    sender_title = parameters.get('sender_title', '')
    sender_company = parameters.get('sender_company', '')
    sender_address = parameters.get('sender_address', '')
    sender_phone = parameters.get('sender_phone', '')
    sender_email = parameters.get('sender_email', '')
    
    recipient_name = parameters.get('recipient_name', '')
    recipient_title = parameters.get('recipient_title', '')
    recipient_company = parameters.get('recipient_company', '')
    recipient_address = parameters.get('recipient_address', '')
    
    date = parameters.get('date', '')
    subject = parameters.get('subject', '')
    intent_type = parameters.get('intent_type', '')
    
    introduction = parameters.get('introduction', '')
    background = parameters.get('background', '')
    intent_details = parameters.get('intent_details', '')
    timeline = parameters.get('timeline', '')
    terms_conditions = parameters.get('terms_conditions', '')
    confidentiality = parameters.get('confidentiality', '')
    conclusion = parameters.get('conclusion', '')

    # Generate HTML document with dynamic styling
    document = f"""
    <div style="max-width: 800px; margin: 0 auto; font-family: Arial, sans-serif;">
        <!-- Sender Information -->
        <div style="text-align: left; margin-bottom: 30px;">
            <p>{sender_name}<br>
            {sender_title}<br>
            {sender_company}<br>
            {sender_address}<br>
            {sender_phone}<br>
            {sender_email}</p>
        </div>
        
        <!-- Date -->
        <div style="margin-bottom: 30px;">
            <p>{date}</p>
        </div>
        
        <!-- Recipient Information -->
        <div style="margin-bottom: 30px;">
            <p>{recipient_name}<br>
            {recipient_title}<br>
            {recipient_company}<br>
            {recipient_address}</p>
        </div>
        
        <!-- Subject -->
        <div style="margin-bottom: 30px;">
            <p><strong>Subject:</strong> {subject}</p>
        </div>
        
        <!-- Salutation -->
        <div style="margin-bottom: 30px;">
            <p>Dear {recipient_name},</p>
        </div>
        
        <!-- Introduction -->
        <div style="margin-bottom: 20px;">
            <p>{introduction}</p>
        </div>
        
        <!-- Background -->
        <div style="margin-bottom: 20px;">
            <h3 style="color: var(--primary-color, #2E86C1);">Background</h3>
            <p>{background}</p>
        </div>
        
        <!-- Intent Details -->
        <div style="margin-bottom: 20px;">
            <h3 style="color: var(--primary-color, #2E86C1);">Intent Details</h3>
            <p>{intent_details}</p>
        </div>
        
        <!-- Timeline -->
        <div style="margin-bottom: 20px;">
            <h3 style="color: var(--primary-color, #2E86C1);">Proposed Timeline</h3>
            <p>{timeline}</p>
        </div>
    """
    
    # Add terms and conditions if provided
    if terms_conditions:
        document += f"""
        <div style="margin-bottom: 20px;">
            <h3 style="color: var(--primary-color, #2E86C1);">Terms and Conditions</h3>
            <p>{terms_conditions}</p>
        </div>
        """
    
    # Add confidentiality clause if provided
    if confidentiality:
        document += f"""
        <div style="margin-bottom: 20px;">
            <h3 style="color: var(--primary-color, #2E86C1);">Confidentiality</h3>
            <p>{confidentiality}</p>
        </div>
        """
    
    # Add conclusion
    document += f"""
        <div style="margin-bottom: 30px;">
            <p>{conclusion}</p>
        </div>
        
        <!-- Closing -->
        <div style="margin-top: 50px;">
            <p>Sincerely,</p>
            <div style="margin-top: 30px;">
                <p>____________________<br>
                {sender_name}<br>
                {sender_title}<br>
                {sender_company}</p>
            </div>
        </div>
    </div>
    
    <style>
    :root {{
        --primary-color: #2E86C1;
        --secondary-color: #2874A6;
    }}
    </style>
    """
    
    return document
