# NDA (Non-Disclosure Agreement) Template

# Define the parameter structure for this document type
PARAMETERS = [
    {
        "section": "General Information",
        "fields": [
            {
                "id": "agreement_date",
                "label": "Agreement Date",
                "type": "date",
                "required": True,
                "help": "Date when this NDA goes into effect"
            },
            {
                "id": "expiration_date",
                "label": "Expiration Date (Optional)",
                "type": "date",
                "required": False,
                "help": "Date when this NDA expires (leave blank for no expiration)"
            }
        ]
    },
    {
        "section": "First Party (Disclosing Party)",
        "fields": [
            {
                "id": "party1_name",
                "label": "Name",
                "type": "text",
                "required": True,
                "help": "Full legal name of the disclosing party (individual or company)"
            },
            {
                "id": "party1_address",
                "label": "Address",
                "type": "textarea",
                "required": True,
                "help": "Full address of the disclosing party"
            },
            {
                "id": "party1_type",
                "label": "Entity Type",
                "type": "select",
                "options": ["Individual", "Corporation", "Limited Liability Company", "Partnership", "Other"],
                "required": True,
                "help": "Legal classification of the disclosing party"
            },
            {
                "id": "party1_state",
                "label": "State of Incorporation/Residence",
                "type": "text",
                "required": True,
                "help": "State where the disclosing party is incorporated or resides"
            }
        ]
    },
    {
        "section": "Second Party (Receiving Party)",
        "fields": [
            {
                "id": "party2_name",
                "label": "Name",
                "type": "text",
                "required": True,
                "help": "Full legal name of the receiving party (individual or company)"
            },
            {
                "id": "party2_address",
                "label": "Address",
                "type": "textarea",
                "required": True,
                "help": "Full address of the receiving party"
            },
            {
                "id": "party2_type",
                "label": "Entity Type",
                "type": "select",
                "options": ["Individual", "Corporation", "Limited Liability Company", "Partnership", "Other"],
                "required": True,
                "help": "Legal classification of the receiving party"
            },
            {
                "id": "party2_state",
                "label": "State of Incorporation/Residence",
                "type": "text",
                "required": True,
                "help": "State where the receiving party is incorporated or resides"
            }
        ]
    },
    {
        "section": "Agreement Details",
        "fields": [
            {
                "id": "purpose",
                "label": "Purpose of Disclosure",
                "type": "textarea",
                "required": True,
                "help": "Describe why confidential information is being shared"
            },
            {
                "id": "confidential_info_definition",
                "label": "Definition of Confidential Information",
                "type": "textarea",
                "required": True,
                "default": "Any information disclosed by Disclosing Party to Receiving Party, either directly or indirectly, in writing, orally or by any other means, that is designated as confidential or that reasonably should be understood to be confidential given the nature of the information and the circumstances of disclosure.",
                "help": "Define what constitutes confidential information under this agreement"
            },
            {
                "id": "governing_law",
                "label": "Governing Law (State)",
                "type": "text",
                "required": True,
                "help": "State whose laws will govern this agreement"
            },
            {
                "id": "term_years",
                "label": "Confidentiality Term (Years)",
                "type": "number",
                "required": True,
                "default": 3,
                "help": "Number of years the confidentiality obligations will remain in effect"
            }
        ]
    }
]

def generate(parameters):
    """
    Generate an NDA document based on the provided parameters
    
    Args:
        parameters: A dictionary containing all the parameter values
        
    Returns:
        HTML content for the document
    """
    # Format dates
    agreement_date = parameters.get("agreement_date", "")
    if isinstance(agreement_date, str):
        formatted_agreement_date = agreement_date
    else:
        formatted_agreement_date = agreement_date.strftime("%B %d, %Y") if agreement_date else ""
    
    expiration_date = parameters.get("expiration_date", "")
    formatted_expiration_date = ""
    if expiration_date:
        if isinstance(expiration_date, str):
            formatted_expiration_date = expiration_date
        else:
            formatted_expiration_date = expiration_date.strftime("%B %d, %Y")
    
    # Get parameters with defaults
    party1_name = parameters.get("party1_name", "[DISCLOSING PARTY NAME]")
    party1_address = parameters.get("party1_address", "[DISCLOSING PARTY ADDRESS]")
    party1_type = parameters.get("party1_type", "Corporation")
    party1_state = parameters.get("party1_state", "[STATE]")
    
    party2_name = parameters.get("party2_name", "[RECEIVING PARTY NAME]")
    party2_address = parameters.get("party2_address", "[RECEIVING PARTY ADDRESS]")
    party2_type = parameters.get("party2_type", "Corporation")
    party2_state = parameters.get("party2_state", "[STATE]")
    
    purpose = parameters.get("purpose", "[PURPOSE OF DISCLOSURE]")
    confidential_info = parameters.get("confidential_info_definition", 
                                      "Any information disclosed by Disclosing Party to Receiving Party, either directly or indirectly, in writing, orally or by any other means, that is designated as confidential or that reasonably should be understood to be confidential given the nature of the information and the circumstances of disclosure.")
    governing_law = parameters.get("governing_law", "[STATE]")
    term_years = parameters.get("term_years", "3")
    
    # Generate the document content
    document = f"""
    <h1 style="text-align: center; margin-bottom: 20px;">NON-DISCLOSURE AGREEMENT</h1>
    
    <p>This Non-Disclosure Agreement (this "Agreement") is made and entered into as of {formatted_agreement_date} by and between:</p>
    
    <p><strong>{party1_name}</strong>, a {party1_type} organized under the laws of {party1_state}, with its principal address at {party1_address} (the "Disclosing Party"), and</p>
    
    <p><strong>{party2_name}</strong>, a {party2_type} organized under the laws of {party2_state}, with its principal address at {party2_address} (the "Receiving Party").</p>
    
    <p>Disclosing Party and Receiving Party are sometimes referred to individually as a "Party" and collectively as the "Parties".</p>
    
    <h3>1. PURPOSE</h3>
    <p>The Parties wish to explore a potential business relationship in connection with {purpose} (the "Purpose"). In connection with the Purpose, Disclosing Party may disclose to Receiving Party certain confidential technical and business information which Disclosing Party desires Receiving Party to treat as confidential.</p>
    
    <h3>2. CONFIDENTIAL INFORMATION</h3>
    <p>"Confidential Information" means {confidential_info}</p>
    
    <h3>3. OBLIGATIONS OF RECEIVING PARTY</h3>
    <p>Receiving Party shall:</p>
    <p>(a) hold the Confidential Information in strict confidence and take reasonable precautions to protect such Confidential Information;</p>
    <p>(b) not divulge any such Confidential Information to any third party;</p>
    <p>(c) not use any such Confidential Information for any purpose except for the Purpose;</p>
    <p>(d) not copy or reverse engineer any such Confidential Information; and</p>
    <p>(e) limit access to Confidential Information to employees, agents, and representatives having a need to know in connection with the Purpose and who are bound by confidentiality obligations at least as restrictive as those contained herein.</p>
    
    <h3>4. TERM AND TERMINATION</h3>
    <p>This Agreement shall remain in effect for {term_years} years from the date of disclosure of Confidential Information.
    """
    
    if formatted_expiration_date:
        document += f" In any case, this Agreement will expire on {formatted_expiration_date}."
    
    document += f"""
    </p>
    <p>Notwithstanding the foregoing, Receiving Party's obligations with respect to Confidential Information that constitutes a trade secret shall continue until such information ceases to be a trade secret.</p>
    
    <h3>5. EXCEPTIONS TO CONFIDENTIALITY</h3>
    <p>The obligations of Receiving Party under this Agreement shall not apply to information that:</p>
    <p>(a) was in the public domain at the time it was disclosed or subsequently enters the public domain through no fault of Receiving Party;</p>
    <p>(b) was known to Receiving Party at the time of disclosure as evidenced by its written records;</p>
    <p>(c) is independently developed by Receiving Party without use of or reference to the Confidential Information;</p>
    <p>(d) becomes known to Receiving Party from a source other than Disclosing Party without breach of this Agreement; or</p>
    <p>(e) is disclosed pursuant to a valid order of a court or other governmental body, provided that Receiving Party provides prompt notice to Disclosing Party of such required disclosure.</p>
    
    <h3>6. RETURN OF MATERIALS</h3>
    <p>All documents and other tangible objects containing or representing Confidential Information, including all copies, notes or summaries thereof, shall be promptly returned to Disclosing Party upon request or destroyed by Receiving Party, at Disclosing Party's option and discretion.</p>
    
    <h3>7. NO RIGHTS GRANTED</h3>
    <p>Nothing in this Agreement shall be construed as granting any rights under any patent, copyright, trade secret or other intellectual property right, nor shall this Agreement grant Receiving Party any rights in or to Disclosing Party's Confidential Information, except the limited right to use such information in accordance with this Agreement.</p>
    
    <h3>8. GOVERNING LAW</h3>
    <p>This Agreement shall be governed by and construed in accordance with the laws of the State of {governing_law}, without regard to conflicts of law principles.</p>
    
    <h3>9. REMEDIES</h3>
    <p>The Parties acknowledge and agree that a breach of this Agreement by Receiving Party may cause irreparable harm to Disclosing Party and that Disclosing Party shall be entitled to seek injunctive relief in addition to any other remedies available at law or in equity.</p>
    
    <h3>10. ENTIRE AGREEMENT</h3>
    <p>This Agreement constitutes the entire agreement between the Parties with respect to the subject matter hereof and supersedes all prior or contemporaneous agreements, understandings, negotiations, and discussions, whether oral or written.</p>
    
    <p>IN WITNESS WHEREOF, the Parties have executed this Agreement as of the date first written above.</p>
    
    <div style="display: flex; justify-content: space-between; margin-top: 50px;">
        <div style="width: 45%;">
            <p><strong>DISCLOSING PARTY:</strong></p>
            <p>{party1_name}</p>
            <p>By: ________________________________</p>
            <p>Name: _____________________________</p>
            <p>Title: ______________________________</p>
        </div>
        
        <div style="width: 45%;">
            <p><strong>RECEIVING PARTY:</strong></p>
            <p>{party2_name}</p>
            <p>By: ________________________________</p>
            <p>Name: _____________________________</p>
            <p>Title: ______________________________</p>
        </div>
    </div>
    """
    
    return document
