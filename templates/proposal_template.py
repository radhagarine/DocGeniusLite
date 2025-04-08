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
    """
    Generate a Business Proposal document based on the provided parameters
    
    Args:
        parameters: A dictionary containing all the parameter values
        
    Returns:
        HTML content for the document
    """
    # Format dates
    proposal_date = parameters.get("proposal_date", "")
    if isinstance(proposal_date, str):
        formatted_proposal_date = proposal_date
    else:
        formatted_proposal_date = proposal_date.strftime("%B %d, %Y") if proposal_date else ""
    
    valid_until = parameters.get("valid_until", "")
    if isinstance(valid_until, str):
        formatted_valid_until = valid_until
    else:
        formatted_valid_until = valid_until.strftime("%B %d, %Y") if valid_until else ""
    
    # Get parameters with defaults
    company_name = parameters.get("company_name", "[COMPANY NAME]")
    company_address = parameters.get("company_address", "[COMPANY ADDRESS]")
    company_phone = parameters.get("company_phone", "[COMPANY PHONE]")
    company_email = parameters.get("company_email", "[COMPANY EMAIL]")
    company_website = parameters.get("company_website", "")
    
    client_name = parameters.get("client_name", "[CLIENT NAME]")
    client_address = parameters.get("client_address", "[CLIENT ADDRESS]")
    client_contact_name = parameters.get("client_contact_name", "[CONTACT NAME]")
    client_contact_title = parameters.get("client_contact_title", "")
    client_email = parameters.get("client_email", "[CLIENT EMAIL]")
    
    proposal_id = parameters.get("proposal_id", "")
    proposal_title = parameters.get("proposal_title", "[PROPOSAL TITLE]")
    
    executive_summary = parameters.get("executive_summary", "[EXECUTIVE SUMMARY]")
    problem_statement = parameters.get("problem_statement", "[PROBLEM STATEMENT]")
    
    proposed_solution = parameters.get("proposed_solution", "[PROPOSED SOLUTION]")
    solution_benefits = parameters.get("solution_benefits", "[SOLUTION BENEFITS]")
    deliverables = parameters.get("deliverables", "[DELIVERABLES]")
    
    pricing_structure = parameters.get("pricing_structure", "[PRICING STRUCTURE]")
    payment_terms = parameters.get("payment_terms", "[PAYMENT TERMS]")
    total_price = parameters.get("total_price", "[TOTAL PRICE]")
    
    timeline = parameters.get("timeline", "[TIMELINE]")
    terms_conditions = parameters.get("terms_conditions", "")
    
    company_background = parameters.get("company_background", "")
    experience = parameters.get("experience", "")
    
    conclusion = parameters.get("conclusion", "[CONCLUSION]")
    
    # Generate the document content
    document = f"""
    <div style="font-family: Arial, sans-serif; color: #333;">
        <!-- Header -->
        <div style="text-align: center; margin-bottom: 40px;">
            <h1 style="color: #2E86C1; margin-bottom: 5px;">{proposal_title}</h1>
            <h3 style="color: #666; font-weight: normal; margin-top: 0;">Business Proposal</h3>
            {f'<p>Proposal ID: {proposal_id}</p>' if proposal_id else ''}
            <p>Prepared for: {client_name}</p>
            <p>Prepared by: {company_name}</p>
            <p>Date: {formatted_proposal_date}</p>
            <p>Valid until: {formatted_valid_until}</p>
        </div>
        
        <!-- Company and Client Information -->
        <div style="display: flex; justify-content: space-between; margin-bottom: 30px;">
            <div style="width: 48%;">
                <h3 style="color: #2E86C1; border-bottom: 1px solid #ddd; padding-bottom: 5px;">From</h3>
                <p><strong>{company_name}</strong></p>
                <p>{company_address.replace('\n', '<br>')}</p>
                <p>Phone: {company_phone}</p>
                <p>Email: {company_email}</p>
                {f'<p>Website: {company_website}</p>' if company_website else ''}
            </div>
            
            <div style="width: 48%;">
                <h3 style="color: #2E86C1; border-bottom: 1px solid #ddd; padding-bottom: 5px;">To</h3>
                <p><strong>{client_name}</strong></p>
                <p>{client_address.replace('\n', '<br>')}</p>
                <p>Attention: {client_contact_name}{f', {client_contact_title}' if client_contact_title else ''}</p>
                <p>Email: {client_email}</p>
            </div>
        </div>
        
        <!-- Executive Summary -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px;">Executive Summary</h2>
            <p>{executive_summary}</p>
        </div>
        
        <!-- Problem Statement -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px;">Problem Statement</h2>
            <p>{problem_statement}</p>
        </div>
        
        <!-- Proposed Solution -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px;">Proposed Solution</h2>
            <p>{proposed_solution}</p>
            
            <h3 style="color: #2E86C1; margin-top: 20px;">Key Benefits</h3>
            <p>{solution_benefits}</p>
            
            <h3 style="color: #2E86C1; margin-top: 20px;">Deliverables</h3>
            <p>{deliverables}</p>
        </div>
        
        <!-- Pricing -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px;">Pricing</h2>
            <p>{pricing_structure}</p>
            
            <h3 style="color: #2E86C1; margin-top: 20px;">Payment Terms</h3>
            <p>{payment_terms}</p>
            
            <div style="background-color: #f8f9fa; padding: 15px; border-left: 5px solid #2E86C1; margin-top: 20px;">
                <h3 style="margin-top: 0; color: #2E86C1;">Total Investment: {total_price}</h3>
            </div>
        </div>
        
        <!-- Timeline -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px;">Project Timeline</h2>
            <p>{timeline}</p>
        </div>
    """
    
    # Add optional sections if provided
    if terms_conditions:
        document += f"""
        <!-- Terms and Conditions -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px;">Terms and Conditions</h2>
            <p>{terms_conditions}</p>
        </div>
        """
    
    if company_background or experience:
        document += f"""
        <!-- About Us -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px;">About {company_name}</h2>
        """
        
        if company_background:
            document += f"""
            <h3 style="color: #2E86C1; margin-top: 20px;">Company Background</h3>
            <p>{company_background}</p>
            """
        
        if experience:
            document += f"""
            <h3 style="color: #2E86C1; margin-top: 20px;">Relevant Experience</h3>
            <p>{experience}</p>
            """
        
        document += """
        </div>
        """
    
    # Conclusion
    document += f"""
        <!-- Conclusion -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px;">Conclusion</h2>
            <p>{conclusion}</p>
        </div>
        
        <!-- Signature -->
        <div style="margin-top: 50px; display: flex; justify-content: space-between;">
            <div style="width: 45%;">
                <p style="border-top: 1px solid #333; padding-top: 10px;">Authorized Signature for {company_name}</p>
                <p>Date: _______________</p>
            </div>
            
            <div style="width: 45%;">
                <p style="border-top: 1px solid #333; padding-top: 10px;">Accepted by {client_name}</p>
                <p>Date: _______________</p>
            </div>
        </div>
        
        <!-- Footer -->
        <div style="margin-top: 50px; text-align: center; font-size: 0.8em; color: #666;">
            <p>© {company_name} | {company_phone} | {company_email}</p>
        </div>
    </div>
    """
    
    return document
