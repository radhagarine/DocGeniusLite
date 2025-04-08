# Scope of Work Template

# Define the parameter structure for this document type
PARAMETERS = [
    {
        "section": "Project Information",
        "fields": [
            {
                "id": "project_name",
                "label": "Project Name",
                "type": "text",
                "required": True,
                "help": "Name of the project"
            },
            {
                "id": "project_number",
                "label": "Project Number/ID",
                "type": "text",
                "required": False,
                "help": "Unique identifier for the project (if applicable)"
            },
            {
                "id": "document_date",
                "label": "Document Date",
                "type": "date",
                "required": True,
                "help": "Date when this scope of work is issued"
            }
        ]
    },
    {
        "section": "Parties",
        "fields": [
            {
                "id": "client_name",
                "label": "Client Name",
                "type": "text",
                "required": True,
                "help": "Full name of the client (individual or organization)"
            },
            {
                "id": "client_address",
                "label": "Client Address",
                "type": "textarea",
                "required": True,
                "help": "Complete address of the client"
            },
            {
                "id": "client_contact",
                "label": "Client Contact Person",
                "type": "text",
                "required": True,
                "help": "Name of the primary contact person at the client"
            },
            {
                "id": "client_email",
                "label": "Client Email",
                "type": "text",
                "required": True,
                "help": "Email address of the client contact"
            },
            {
                "id": "client_phone",
                "label": "Client Phone",
                "type": "text",
                "required": True,
                "help": "Phone number of the client contact"
            },
            {
                "id": "contractor_name",
                "label": "Contractor/Vendor Name",
                "type": "text",
                "required": True,
                "help": "Your name or your company's name"
            },
            {
                "id": "contractor_address",
                "label": "Contractor/Vendor Address",
                "type": "textarea",
                "required": True,
                "help": "Your complete address or your company's address"
            },
            {
                "id": "contractor_contact",
                "label": "Contractor Contact Person",
                "type": "text",
                "required": True,
                "help": "Name of the primary contact person at the contractor"
            },
            {
                "id": "contractor_email",
                "label": "Contractor Email",
                "type": "text",
                "required": True,
                "help": "Email address of the contractor contact"
            },
            {
                "id": "contractor_phone",
                "label": "Contractor Phone",
                "type": "text",
                "required": True,
                "help": "Phone number of the contractor contact"
            }
        ]
    },
    {
        "section": "Project Overview",
        "fields": [
            {
                "id": "project_description",
                "label": "Project Description",
                "type": "textarea",
                "required": True,
                "help": "General description and purpose of the project"
            },
            {
                "id": "project_objectives",
                "label": "Project Objectives",
                "type": "textarea",
                "required": True,
                "help": "Specific objectives the project aims to achieve"
            }
        ]
    },
    {
        "section": "Scope of Services",
        "fields": [
            {
                "id": "scope_overview",
                "label": "Scope Overview",
                "type": "textarea",
                "required": True,
                "help": "High-level overview of the work to be performed"
            },
            {
                "id": "included_work",
                "label": "Work Included",
                "type": "textarea",
                "required": True,
                "help": "Detailed description of tasks, deliverables, and services to be provided"
            },
            {
                "id": "excluded_work",
                "label": "Work Excluded",
                "type": "textarea",
                "required": False,
                "help": "Tasks or deliverables specifically excluded from the scope (if applicable)"
            }
        ]
    },
    {
        "section": "Deliverables",
        "fields": [
            {
                "id": "deliverables",
                "label": "Deliverables",
                "type": "textarea",
                "required": True,
                "help": "List of all deliverables with descriptions"
            },
            {
                "id": "deliverable_format",
                "label": "Deliverable Format",
                "type": "textarea",
                "required": False,
                "help": "Format specifications for deliverables (if applicable)"
            },
            {
                "id": "acceptance_criteria",
                "label": "Acceptance Criteria",
                "type": "textarea",
                "required": True,
                "help": "Criteria for determining whether deliverables meet requirements"
            }
        ]
    },
    {
        "section": "Timeline",
        "fields": [
            {
                "id": "project_start",
                "label": "Project Start Date",
                "type": "date",
                "required": True,
                "help": "Date when work will begin"
            },
            {
                "id": "project_end",
                "label": "Project End Date",
                "type": "date",
                "required": True,
                "help": "Expected completion date"
            },
            {
                "id": "milestones",
                "label": "Key Milestones",
                "type": "textarea",
                "required": True,
                "help": "List of key milestones with dates"
            }
        ]
    },
    {
        "section": "Budget and Payment",
        "fields": [
            {
                "id": "fee_structure",
                "label": "Fee Structure",
                "type": "select",
                "options": ["Fixed Fee", "Time and Materials", "Hourly Rate", "Monthly Retainer", "Other"],
                "required": True,
                "help": "Type of fee structure for this project"
            },
            {
                "id": "total_cost",
                "label": "Total Cost",
                "type": "text",
                "required": True,
                "help": "Total cost for the entire project"
            },
            {
                "id": "payment_schedule",
                "label": "Payment Schedule",
                "type": "textarea",
                "required": True,
                "help": "Schedule and terms for payments"
            },
            {
                "id": "expenses",
                "label": "Expenses",
                "type": "textarea",
                "required": False,
                "help": "Policy for reimbursable expenses (if applicable)"
            }
        ]
    },
    {
        "section": "Additional Terms",
        "fields": [
            {
                "id": "change_management",
                "label": "Change Management Process",
                "type": "textarea",
                "required": True,
                "help": "Process for handling changes to the scope"
            },
            {
                "id": "responsibilities",
                "label": "Client Responsibilities",
                "type": "textarea",
                "required": False,
                "help": "Specific responsibilities of the client"
            },
            {
                "id": "assumptions",
                "label": "Assumptions",
                "type": "textarea",
                "required": False,
                "help": "Assumptions made in creating this scope of work"
            },
            {
                "id": "termination",
                "label": "Termination Clause",
                "type": "textarea",
                "required": False,
                "help": "Terms for early termination of the project"
            }
        ]
    }
]

def generate(parameters):
    """
    Generate a Scope of Work document based on the provided parameters
    
    Args:
        parameters: A dictionary containing all the parameter values
        
    Returns:
        HTML content for the document
    """
    # Format dates
    document_date = parameters.get("document_date", "")
    if isinstance(document_date, str):
        formatted_document_date = document_date
    else:
        formatted_document_date = document_date.strftime("%B %d, %Y") if document_date else ""
    
    project_start = parameters.get("project_start", "")
    if isinstance(project_start, str):
        formatted_project_start = project_start
    else:
        formatted_project_start = project_start.strftime("%B %d, %Y") if project_start else ""
    
    project_end = parameters.get("project_end", "")
    if isinstance(project_end, str):
        formatted_project_end = project_end
    else:
        formatted_project_end = project_end.strftime("%B %d, %Y") if project_end else ""
    
    # Get parameters with defaults
    project_name = parameters.get("project_name", "[PROJECT NAME]")
    project_number = parameters.get("project_number", "")
    
    client_name = parameters.get("client_name", "[CLIENT NAME]")
    client_address = parameters.get("client_address", "[CLIENT ADDRESS]")
    client_contact = parameters.get("client_contact", "[CLIENT CONTACT]")
    client_email = parameters.get("client_email", "[CLIENT EMAIL]")
    client_phone = parameters.get("client_phone", "[CLIENT PHONE]")
    
    contractor_name = parameters.get("contractor_name", "[CONTRACTOR NAME]")
    contractor_address = parameters.get("contractor_address", "[CONTRACTOR ADDRESS]")
    contractor_contact = parameters.get("contractor_contact", "[CONTRACTOR CONTACT]")
    contractor_email = parameters.get("contractor_email", "[CONTRACTOR EMAIL]")
    contractor_phone = parameters.get("contractor_phone", "[CONTRACTOR PHONE]")
    
    project_description = parameters.get("project_description", "[PROJECT DESCRIPTION]")
    project_objectives = parameters.get("project_objectives", "[PROJECT OBJECTIVES]")
    
    scope_overview = parameters.get("scope_overview", "[SCOPE OVERVIEW]")
    included_work = parameters.get("included_work", "[INCLUDED WORK]")
    excluded_work = parameters.get("excluded_work", "")
    
    deliverables = parameters.get("deliverables", "[DELIVERABLES]")
    deliverable_format = parameters.get("deliverable_format", "")
    acceptance_criteria = parameters.get("acceptance_criteria", "[ACCEPTANCE CRITERIA]")
    
    milestones = parameters.get("milestones", "[MILESTONES]")
    
    fee_structure = parameters.get("fee_structure", "Fixed Fee")
    total_cost = parameters.get("total_cost", "[TOTAL COST]")
    payment_schedule = parameters.get("payment_schedule", "[PAYMENT SCHEDULE]")
    expenses = parameters.get("expenses", "")
    
    change_management = parameters.get("change_management", "[CHANGE MANAGEMENT PROCESS]")
    responsibilities = parameters.get("responsibilities", "")
    assumptions = parameters.get("assumptions", "")
    termination = parameters.get("termination", "")
    
    # Generate the document content
    document = f"""
    <div style="font-family: Arial, sans-serif; color: #333;">
        <!-- Header -->
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #2E86C1;">SCOPE OF WORK</h1>
            <h2 style="color: #555;">{project_name}</h2>
            {f'<p>Project ID: {project_number}</p>' if project_number else ''}
            <p>Date: {formatted_document_date}</p>
        </div>
        
        <!-- Party Information -->
        <div style="display: flex; justify-content: space-between; margin-bottom: 30px;">
            <div style="width: 48%;">
                <h3 style="color: #2E86C1; border-bottom: 1px solid #ddd; padding-bottom: 5px;">Client</h3>
                <p><strong>{client_name}</strong></p>
                <p>{client_address.replace('\n', '<br>')}</p>
                <p><strong>Contact:</strong> {client_contact}</p>
                <p><strong>Email:</strong> {client_email}</p>
                <p><strong>Phone:</strong> {client_phone}</p>
            </div>
            
            <div style="width: 48%;">
                <h3 style="color: #2E86C1; border-bottom: 1px solid #ddd; padding-bottom: 5px;">Contractor</h3>
                <p><strong>{contractor_name}</strong></p>
                <p>{contractor_address.replace('\n', '<br>')}</p>
                <p><strong>Contact:</strong> {contractor_contact}</p>
                <p><strong>Email:</strong> {contractor_email}</p>
                <p><strong>Phone:</strong> {contractor_phone}</p>
            </div>
        </div>
        
        <!-- Project Overview -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px;">1. PROJECT OVERVIEW</h2>
            
            <h3 style="color: #2E86C1; margin-top: 20px;">1.1 Project Description</h3>
            <p>{project_description}</p>
            
            <h3 style="color: #2E86C1; margin-top: 20px;">1.2 Project Objectives</h3>
            <p>{project_objectives}</p>
        </div>
        
        <!-- Scope of Services -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px;">2. SCOPE OF SERVICES</h2>
            
            <h3 style="color: #2E86C1; margin-top: 20px;">2.1 Scope Overview</h3>
            <p>{scope_overview}</p>
            
            <h3 style="color: #2E86C1; margin-top: 20px;">2.2 Work Included</h3>
            <p>{included_work}</p>
    """
    
    if excluded_work:
        document += f"""
            <h3 style="color: #2E86C1; margin-top: 20px;">2.3 Work Excluded</h3>
            <p>{excluded_work}</p>
        """
    
    document += f"""
        </div>
        
        <!-- Deliverables -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px;">3. DELIVERABLES</h2>
            
            <h3 style="color: #2E86C1; margin-top: 20px;">3.1 List of Deliverables</h3>
            <p>{deliverables}</p>
    """
    
    if deliverable_format:
        document += f"""
            <h3 style="color: #2E86C1; margin-top: 20px;">3.2 Deliverable Format</h3>
            <p>{deliverable_format}</p>
        """
    
    document += f"""
            <h3 style="color: #2E86C1; margin-top: 20px;">3.3 Acceptance Criteria</h3>
            <p>{acceptance_criteria}</p>
        </div>
        
        <!-- Timeline -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px;">4. TIMELINE</h2>
            
            <p><strong>Project Start Date:</strong> {formatted_project_start}</p>
            <p><strong>Project End Date:</strong> {formatted_project_end}</p>
            
            <h3 style="color: #2E86C1; margin-top: 20px;">4.1 Key Milestones</h3>
            <p>{milestones}</p>
        </div>
        
        <!-- Budget and Payment -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px;">5. BUDGET AND PAYMENT</h2>
            
            <p><strong>Fee Structure:</strong> {fee_structure}</p>
            <p><strong>Total Cost:</strong> {total_cost}</p>
            
            <h3 style="color: #2E86C1; margin-top: 20px;">5.1 Payment Schedule</h3>
            <p>{payment_schedule}</p>
    """
    
    if expenses:
        document += f"""
            <h3 style="color: #2E86C1; margin-top: 20px;">5.2 Expenses</h3>
            <p>{expenses}</p>
        """
    
    document += f"""
        </div>
        
        <!-- Additional Terms -->
        <div style="margin-bottom: 30px;">
            <h2 style="color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px;">6. ADDITIONAL TERMS</h2>
            
            <h3 style="color: #2E86C1; margin-top: 20px;">6.1 Change Management</h3>
            <p>{change_management}</p>
    """
    
    if responsibilities:
        document += f"""
            <h3 style="color: #2E86C1; margin-top: 20px;">6.2 Client Responsibilities</h3>
            <p>{responsibilities}</p>
        """
    
    if assumptions:
        document += f"""
            <h3 style="color: #2E86C1; margin-top: 20px;">6.3 Assumptions</h3>
            <p>{assumptions}</p>
        """
    
    if termination:
        document += f"""
            <h3 style="color: #2E86C1; margin-top: 20px;">6.4 Termination</h3>
            <p>{termination}</p>
        """
    
    document += f"""
        </div>
        
        <!-- Signatures -->
        <div style="margin-top: 50px;">
            <h2 style="color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px;">7. AGREEMENT</h2>
            <p>By signing below, the parties agree to the terms and conditions set forth in this Scope of Work document.</p>
            
            <div style="display: flex; justify-content: space-between; margin-top: 40px;">
                <div style="width: 45%;">
                    <p style="border-top: 1px solid #333; padding-top: 10px;"><strong>For Client: {client_name}</strong></p>
                    <p>Name: ________________________________</p>
                    <p>Title: ________________________________</p>
                    <p>Date: ________________________________</p>
                    <p>Signature: ________________________________</p>
                </div>
                
                <div style="width: 45%;">
                    <p style="border-top: 1px solid #333; padding-top: 10px;"><strong>For Contractor: {contractor_name}</strong></p>
                    <p>Name: ________________________________</p>
                    <p>Title: ________________________________</p>
                    <p>Date: ________________________________</p>
                    <p>Signature: ________________________________</p>
                </div>
            </div>
        </div>
    </div>
    """
    
    return document
