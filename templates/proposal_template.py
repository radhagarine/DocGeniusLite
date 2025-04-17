# Business Proposal Template

# Define the parameter structure for this document type
PARAMETERS = [
    {
        "section": "Company Information",
        "fields": [
            {
                "id": "company_name",
                "label": "Company Name",
                "type": "text",
                "required": True,
                "help": "Your company or business name"
            },
            {
                "id": "company_address",
                "label": "Company Address",
                "type": "textarea",
                "required": True,
                "help": "Your complete company address"
            },
            {
                "id": "company_phone",
                "label": "Company Phone",
                "type": "text",
                "required": True,
                "help": "Your company phone number"
            },
            {
                "id": "company_email",
                "label": "Company Email",
                "type": "text",
                "required": True,
                "help": "Your company email address"
            },
            {
                "id": "company_website",
                "label": "Company Website",
                "type": "text",
                "required": False,
                "help": "Your company website URL"
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
                "id": "client_contact_name",
                "label": "Client Contact Person",
                "type": "text",
                "required": True,
                "help": "Name of the primary contact person at the client"
            },
            {
                "id": "client_contact_title",
                "label": "Client Contact Title",
                "type": "text",
                "required": False,
                "help": "Title of the contact person at the client"
            },
            {
                "id": "client_email",
                "label": "Client Email",
                "type": "text",
                "required": True,
                "help": "Email address of the client contact"
            }
        ]
    },
    {
        "section": "Proposal Details",
        "fields": [
            {
                "id": "proposal_date",
                "label": "Proposal Date",
                "type": "date",
                "required": True,
                "help": "Date of the proposal submission"
            },
            {
                "id": "proposal_id",
                "label": "Proposal ID",
                "type": "text",
                "required": False,
                "help": "Unique identifier for this proposal (e.g., PROP-2023-001)"
            },
            {
                "id": "proposal_title",
                "label": "Proposal Title",
                "type": "text",
                "required": True,
                "help": "A concise title for your proposal"
            },
            {
                "id": "valid_until",
                "label": "Valid Until",
                "type": "date",
                "required": True,
                "help": "Date until which this proposal is valid"
            }
        ]
    },
    {
        "section": "Executive Summary",
        "fields": [
            {
                "id": "executive_summary",
                "label": "Executive Summary",
                "type": "textarea",
                "required": True,
                "help": "A brief overview of the proposal (1-2 paragraphs)"
            }
        ]
    },
    {
        "section": "Problem Statement",
        "fields": [
            {
                "id": "problem_statement",
                "label": "Problem Statement",
                "type": "textarea",
                "required": True,
                "help": "Describe the client's problem or need that your proposal addresses"
            }
        ]
    },
    {
        "section": "Proposed Solution",
        "fields": [
            {
                "id": "proposed_solution",
                "label": "Proposed Solution",
                "type": "textarea",
                "required": True,
                "help": "Detailed description of your proposed solution"
            },
            {
                "id": "solution_benefits",
                "label": "Benefits",
                "type": "textarea",
                "required": True,
                "help": "Key benefits of your proposed solution"
            },
            {
                "id": "deliverables",
                "label": "Deliverables",
                "type": "textarea",
                "required": True,
                "help": "List of specific deliverables included in the proposal"
            }
        ]
    },
    {
        "section": "Pricing",
        "fields": [
            {
                "id": "pricing_structure",
                "label": "Pricing Structure",
                "type": "textarea",
                "required": True,
                "help": "Detailed breakdown of costs and pricing"
            },
            {
                "id": "payment_terms",
                "label": "Payment Terms",
                "type": "textarea",
                "required": True,
                "help": "Terms and schedule for payments"
            },
            {
                "id": "total_price",
                "label": "Total Price",
                "type": "text",
                "required": True,
                "help": "The total price for the proposed solution"
            }
        ]
    },
    {
        "section": "Timeline",
        "fields": [
            {
                "id": "timeline",
                "label": "Project Timeline",
                "type": "textarea",
                "required": True,
                "help": "Timeline for implementation and major milestones"
            }
        ]
    },
    {
        "section": "Terms and Conditions",
        "fields": [
            {
                "id": "terms_conditions",
                "label": "Terms and Conditions",
                "type": "textarea",
                "required": False,
                "help": "Any additional terms and conditions"
            }
        ]
    },
    {
        "section": "About Us",
        "fields": [
            {
                "id": "company_background",
                "label": "Company Background",
                "type": "textarea",
                "required": False,
                "help": "Brief background about your company and qualifications"
            },
            {
                "id": "experience",
                "label": "Relevant Experience",
                "type": "textarea",
                "required": False,
                "help": "Description of relevant past experience or case studies"
            }
        ]
    },
    {
        "section": "Conclusion",
        "fields": [
            {
                "id": "conclusion",
                "label": "Conclusion",
                "type": "textarea",
                "required": True,
                "help": "Closing statement summarizing key points and next steps"
            }
        ]
    }
]

def generate(parameters):
    """Generate a business proposal document"""
    # Extract parameters
    company_name = parameters.get('company_name', '')
    company_address = parameters.get('company_address', '')
    company_phone = parameters.get('company_phone', '')
    company_email = parameters.get('company_email', '')
    company_website = parameters.get('company_website', '')
    
    client_name = parameters.get('client_name', '')
    client_address = parameters.get('client_address', '')
    client_contact_name = parameters.get('client_contact_name', '')
    client_contact_title = parameters.get('client_contact_title', '')
    client_email = parameters.get('client_email', '')
    
    proposal_date = parameters.get('proposal_date', '')
    proposal_id = parameters.get('proposal_id', '')
    proposal_title = parameters.get('proposal_title', '')
    valid_until = parameters.get('valid_until', '')
    
    executive_summary = parameters.get('executive_summary', '')
    problem_statement = parameters.get('problem_statement', '')
    proposed_solution = parameters.get('proposed_solution', '')
    solution_benefits = parameters.get('solution_benefits', '')
    deliverables = parameters.get('deliverables', '')
    
    pricing_structure = parameters.get('pricing_structure', '')
    payment_terms = parameters.get('payment_terms', '')
    total_price = parameters.get('total_price', '')
    
    timeline = parameters.get('timeline', '')
    terms_conditions = parameters.get('terms_conditions', '')
    company_background = parameters.get('company_background', '')
    experience = parameters.get('experience', '')
    conclusion = parameters.get('conclusion', '')

    # Generate HTML document with dynamic styling support
    document = f"""
    <div style="max-width: 800px; margin: 0 auto; font-family: Arial, sans-serif;">
        <!-- Header -->
        <div style="text-align: center; margin-bottom: 40px;">
            <h1 style="color: var(--primary-color, #2E86C1); margin-bottom: 10px;">{proposal_title}</h1>
            <p style="font-size: 1.1em;">Prepared for {client_name}</p>
            <p>Proposal #{proposal_id} | {proposal_date}</p>
        </div>
        
        <!-- Company Information -->
        <div style="display: flex; justify-content: space-between; margin-bottom: 40px;">
            <div>
                <strong>{company_name}</strong><br>
                {company_address}<br>
                {company_phone}<br>
                {company_email}
                {f'<br>{company_website}' if company_website else ''}
            </div>
            <div style="text-align: right;">
                <strong>{client_name}</strong><br>
                {client_address}<br>
                {client_contact_name}
                {f'<br>{client_contact_title}' if client_contact_title else ''}<br>
                {client_email}
            </div>
        </div>
        
        <!-- Executive Summary -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: var(--primary-color, #2E86C1); border-bottom: 2px solid var(--primary-color, #2E86C1); padding-bottom: 5px;">Executive Summary</h2>
            <p>{executive_summary}</p>
        </div>
        
        <!-- Problem Statement -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: var(--primary-color, #2E86C1); border-bottom: 2px solid var(--primary-color, #2E86C1); padding-bottom: 5px;">Problem Statement</h2>
            <p>{problem_statement}</p>
        </div>
        
        <!-- Proposed Solution -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: var(--primary-color, #2E86C1); border-bottom: 2px solid var(--primary-color, #2E86C1); padding-bottom: 5px;">Our Solution</h2>
            <p>{proposed_solution}</p>
            
            <h3 style="color: var(--primary-color, #2E86C1); margin-top: 20px;">Key Benefits</h3>
            <p>{solution_benefits}</p>
            
            <h3 style="color: var(--primary-color, #2E86C1); margin-top: 20px;">Deliverables</h3>
            <p>{deliverables}</p>
        </div>
        
        <!-- Pricing -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: var(--primary-color, #2E86C1); border-bottom: 2px solid var(--primary-color, #2E86C1); padding-bottom: 5px;">Investment</h2>
            <div style="background: rgba(46, 134, 193, 0.1); padding: 20px; border-radius: 5px; margin-top: 20px;">
                <h3 style="color: var(--primary-color, #2E86C1); margin-top: 0;">Total Investment: {total_price}</h3>
                <p><strong>Pricing Structure:</strong><br>{pricing_structure}</p>
                <p><strong>Payment Terms:</strong><br>{payment_terms}</p>
            </div>
        </div>
        
        <!-- Timeline -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: var(--primary-color, #2E86C1); border-bottom: 2px solid var(--primary-color, #2E86C1); padding-bottom: 5px;">Project Timeline</h2>
            <p>{timeline}</p>
            <p><strong>Valid Until:</strong> {valid_until}</p>
        </div>
    """
    
    if terms_conditions:
        document += f"""
        <!-- Terms and Conditions -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: var(--primary-color, #2E86C1); border-bottom: 2px solid var(--primary-color, #2E86C1); padding-bottom: 5px;">Terms and Conditions</h2>
            <p>{terms_conditions}</p>
        </div>
        """
    
    if company_background or experience:
        document += f"""
        <!-- About Us -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: var(--primary-color, #2E86C1); border-bottom: 2px solid var(--primary-color, #2E86C1); padding-bottom: 5px;">About {company_name}</h2>
        """
        
        if company_background:
            document += f"""
            <h3 style="color: var(--primary-color, #2E86C1); margin-top: 20px;">Company Background</h3>
            <p>{company_background}</p>
            """
        
        if experience:
            document += f"""
            <h3 style="color: var(--primary-color, #2E86C1); margin-top: 20px;">Relevant Experience</h3>
            <p>{experience}</p>
            """
        
        document += """
        </div>
        """
    
    # Add conclusion
    document += f"""
        <!-- Conclusion -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: var(--primary-color, #2E86C1); border-bottom: 2px solid var(--primary-color, #2E86C1); padding-bottom: 5px;">Next Steps</h2>
            <p>{conclusion}</p>
        </div>
    """
    
    # Add footer
    document += f"""
        <!-- Footer -->
        <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #ccc; color: #666;">
            <p>For questions about this proposal, please contact:</p>
            <p><strong>{company_name}</strong><br>
            {company_email} | {company_phone}</p>
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
