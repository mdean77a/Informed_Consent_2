def summary_query():
    summary_query = """ 
    Please write a summary of the protocol that can be used as the introduction to an informed
    consent document for a patient to participate in the study described in the protocol.  This
    summary should be between 500 and 1000 words in length, and should be understandable by a normally
    intelligent adult patient.  You must explain any medical or technical terms in a way
    that a high school graduate can understand. The summary should briefly explain the study, the rationale for the study,
    the risks and benefits of participation, and that participation is entirely voluntary.

    Start the summary with a level 2 Markdown header (##) titled "Study Summary". Then continue with
    the content without any further subheadings. Produce the entire summary in Markdown format so it 
    can be nicely printed for the reader.

    You should assume that the consent form is addressed to the parent of a potentially eligible
    child, and the very beginnning of the summary should indicate that they are being invited to allow
    their child to participate because the child is potentially eligible. State why their child is potentially
    eligible.  

    All the details of this introductory summary should be specific for this protocol.

    """
    return summary_query

def background_query():

    background_query = """ 
    Please write a summary of the protocol that can be used as the background section of an informed
    consent document for a patient to participate in the study described in the protocol.  This
    summary should be between 500 and 1000 words in length, and should be understandable by a normally
    intelligent adult patient.  You must explain any medical or technical terms in a way
    that a high school graduate can understand. The summary should briefly explain why this patient is being
    approached to be in the study, including a brief description of the disease that is being studied in the 
    protocol, a description of the study interventions, and the scientific reasons that the investigators believe
    the intervention might help the patient.  

    Do not include the specific study procedures in this summary, because this will be presented in a different section of 
    the informed consent document.  You also do not need to mention that participation is voluntary, nor
    the specific risks and benefits of the study, because this information is being presented in a different
    part of the informed consent document.

    Start the summary with a level 2 Markdown header (##) titled "Background". Then continue with
    the content without any further subheadings. Produce the entire summary in Markdown format so it 
    can be nicely printed for the reader. 

    All the details of this background summary should be specific for this protocol.

    """
    return background_query

def number_of_participants_query():

    number_of_participants_query = """ 
    Please write a summary of the protocol that can be used 
    for the "number of participants" section of the informed consent document.  This should include where the
    study is being conducted (for example, at this hospital, or in a network, or in multiple hospitals), the funding source
    (often the NIH), the total number of participants that are planned to be enrolled in the study,
    and the total period of the time that the study is expected to enroll subjects. This summary should not require more than 200 words.

    Start the summary with a level 2 Markdown header (##) titled "Number of Participants". Then continue with
    the content without any further subheadings. Produce the entire summary in Markdown format so it 
    can be nicely printed for the reader. 

    All the details of this number of participants summary should be specific for this protocol.

    """
    return number_of_participants_query

def study_procedures_query():
    study_procedures_query = """ 
    Please write a detailed summary of all the study procedures that will be carried out in this protocol.  This will
    be used for the "study procedures" section of the informed consent document that the patient will read when deciding
    whether to participate in the study, so it is important that all significant procedures be included.  
    Make sure that everything will be understandable to the reader, who is not trained in medicine.  Do not write
    the summary as if it is in third person - write it like you are speaking directly to the patient (i.e. use "you" instead 
    of the "patient", with correct grammar of course.)  Do not include a welcome to the study, or discussion about
    participation being voluntary, as that information is in a different part of the consent document.  Do not include
    risks and benefits as these are presented in a different part of the consent document.  Please be detailed, as it is 
    important that the patient understand each procedure.
    The length of this summary is usually
    2000 to 3000 words.

    Start the summary with a level 2 Markdown header (##) titled "Study Procedures", and then continue the section with subheadings
    that will help organize the information for the reader.  Do not go more than two subheadings deep.

    All the details of study procedures should be specific to this protocol.

    """
    return study_procedures_query

def alt_procedures_query():
    alt_procedures_query = """ 
    Please write a  summary of alternatives to participation in this study.  An example is:

    " Your participation in this study is voluntary.  It is not necessary to be in this study to get care for
    your illness.  Monitoring of immune function is not currently done as part of routine ICU care.  There are no
    other treatments designed to increase immune function of reduce inflammation that are routinely used in 
    children with sepsis."

    Note that this example is purely an example, and your summary must be specific to the protocol. The summary should
    be easily understandable by medically untrained readers.  This section is usually less than 500 words in length.


    Start the summary with a level 2 Markdown header (##) titled "Alternative Procedures", and then continue with
    the content without any further subheadings. Produce the entire summary in Markdown format so it 
    can be nicely printed for the reader. 


    """
    return alt_procedures_query

def risks_query():
    risks_query = """ 
    Please write a detailed summary of the risks of participating in  the study.  This will be used for the
    "Risks" section of the informed consent document.  It is important that all significant risks of study
    participation are described in detail. The summary must be easily readable by untrained readers, so provide
    definitions of technical or medical terms.  Address all the risks by speaking to the patient, not by passively
    mentioning risks to "the patient".  Especially include risks that are associated with the study interventions such
    as drugs or devices, or associated with testing that is done as part of the study.  Also include
    the risks associated with data collection, and also mention "unforeseable risks".

    The length of this risk summary is usually
    2000 to 3000 words.

    Start the summary with a level 2 Markdown header (##) titled "Risks", and then continue the section with subheadings
    that will help organize the information for the reader.  Do not go more than two subheadings deep.

    All the details of study risks should be specific to this protocol.

    """
    return risks_query

def benefits_query():
    benefits_query = """ 
    Please write a  summary of the potential benefits of participating in  the study.  This will be used for the
    "Benefits" section of the informed consent document.  The summary should include potential benefits for the patient
    (addressed as "you"), and potential benefits for others.  Since this is a research study and it is
    not known if the intervention is helpful, it is important to not overstate potential benefits for the patient.

    The length of this risk summary is usually
    500 to 750 words.

    Start the summary with a level 2 Markdown header (##) titled "Benefits",  and then continue 
    with a subheading for "Potential
    Benefits for You" and another subheading for "Potential Benefits for Others".

    All the information of study benefits should be specific to this protocol.

    """
    return benefits_query