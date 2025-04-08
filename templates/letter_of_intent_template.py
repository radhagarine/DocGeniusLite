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
    """
    Generate a Letter of Intent document based on the provided parameters
    
    Args:
        parameters: A dictionary containing all the parameter values
        
    Returns:
        HTML content for the document
    """
    # Format date
    letter_date = parameters.get("letter_date", "")
    if isinstance(letter_date, str):
        formatted_letter_date = letter_date
    else:
        formatted_letter_date = letter_date.strftime("%B %d, %Y") if letter_date else ""
    
    # Get parameters with defaults
    sender_name = parameters.get("sender_name", "[SENDER NAME]")
    sender_address = parameters.get("sender_address", "[SENDER ADDRESS]")
    recipient_name = parameters.get("recipient_name", "[RECIPIENT NAME]")
    recipient_address = parameters.get("recipient_address", "[RECIPIENT ADDRESS]")
    
    subject = parameters.get("subject", "[SUBJECT]")
    intent_type = parameters.get("intent_type", "Business Partnership")
    
    introduction = parameters.get("introduction", "This Letter of Intent (\"LOI\") sets forth the basic terms of a proposed transaction between the parties. While this LOI represents the understanding of the parties regarding the proposed transaction, it is not legally binding except as stated in the 'Binding Provisions' section.")
    transaction_description = parameters.get("transaction_description", "[TRANSACTION DESCRIPTION]")
    proposed_terms = parameters.get("proposed_terms", "[PROPOSED TERMS]")
    timeline = parameters.get("timeline", "[TIMELINE]")
    
    confidentiality = parameters.get("confidentiality", "The parties agree to maintain the confidentiality of any information exchanged in connection with this LOI and the proposed transaction. This confidentiality provision shall be binding regardless of whether the parties proceed with the proposed transaction.")
    exclusivity = parameters.get("exclusivity", "")
    expenses = parameters.get("expenses", "Each party shall bear its own expenses related to this LOI and the proposed transaction, including but not limited to legal, accounting, and advisory fees.")
    governing_law = parameters.get("governing_law", "[STATE/JURISDICTION]")
    
    closing_statement = parameters.get("closing_statement", "We look forward to working together toward a mutually beneficial relationship. If the terms outlined in this Letter of Intent are acceptable, please indicate your agreement by signing below.")
    sender_signatory = parameters.get("sender_signatory", "[SENDER SIGNATORY]")
    sender_title = parameters.get("sender_title", "[SENDER TITLE]")
    recipient_signatory = parameters.get("recipient_signatory", "[RECIPIENT SIGNATORY]")
    recipient_title = parameters.get("recipient_title", "[RECIPIENT TITLE]")
    
    # Generate the document content
    document = f"""
    <div style="font-family: Arial, sans-serif; margin: 1in;">
        <div style="text-align: left; margin-bottom: 1in;">
            <p>{formatted_letter_date}</p>
            <p>{sender_name}<br>{sender_address.replace('\n', '<br>')}</p>
            <br>
            <p>{recipient_name}<br>{recipient_address.replace('\n', '<br>')}</p>
        </div>
        
        <div style="text-align: center; margin-bottom: 1in;">
            <h2>LETTER OF INTENT</h2>
            <h3>Re: {subject}</h3>
        </div>
        
        <div style="text-align: justify;">
            <p>Dear {recipient_name.split()[0] if recipient_name.split() else recipient_name},</p>
            
            <p>{introduction}</p>
            
            <h3>1. Parties</h3>
            <p>This Letter of Intent is between {sender_name} (the "Sender") and {recipient_name} (the "Recipient"), collectively referred to as the "Parties".</p>
            
            <h3>2. Type of Transaction</h3>
            <p>This Letter of Intent relates to a proposed {intent_type.lower()}.</p>
            
            <h3>3. Transaction Description</h3>
            <p>{transaction_description}</p>
            
            <h3>4. Proposed Terms</h3>
            <p>{proposed_terms}</p>
            
            <h3>5. Timeline</h3>
            <p>{timeline}</p>
    """
    
    # Add conditional sections
    if confidentiality:
        document += f"""
            <h3>6. Confidentiality</h3>
            <p>{confidentiality}</p>
        """
    
    if exclusivity:
        document += f"""
            <h3>7. Exclusivity</h3>
            <p>{exclusivity}</p>
        """
    
    if expenses:
        document += f"""
            <h3>8. Expenses</h3>
            <p>{expenses}</p>
        """
    
    document += f"""
            <h3>9. Binding Provisions</h3>
            <p>The Parties acknowledge that this Letter of Intent is non-binding with respect to the transaction contemplated herein, except for the provisions relating to confidentiality, exclusivity (if applicable), expenses, and governing law, which shall be binding upon execution of this Letter of Intent.</p>
            
            <h3>10. Governing Law</h3>
            <p>This Letter of Intent shall be governed by the laws of {governing_law}, without regard to its conflict of laws principles.</p>
            
            <p>{closing_statement}</p>
            
            <p>Sincerely,</p>
            
            <div style="margin-top: 1in;">
                <div style="float: left; width: 45%;">
                    <p><strong>For {sender_name}:</strong></p>
                    <p>________________________________</p>
                    <p>{sender_signatory}, {sender_title}</p>
                    <p>Date: ________________________</p>
                </div>
                
                <div style="float: right; width: 45%;">
                    <p><strong>AGREED AND ACCEPTED:</strong></p>
                    <p><strong>For {recipient_name}:</strong></p>
                    <p>________________________________</p>
                    <p>{recipient_signatory}, {recipient_title}</p>
                    <p>Date: ________________________</p>
                </div>
                <div style="clear: both;"></div>
            </div>
        </div>
    </div>
    """
    
    return document
