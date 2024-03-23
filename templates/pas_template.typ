// Adopted from https://www.bostonscientific.com/content/dam/bostonscientific/Reimbursement/RhythmManagement/pdf/Sample_Prior_Authorization_Letter_for_S-ICD.pdf

#set page(
  paper: "us-letter",
  header: align(right)[
    #image($headerlogo, width: 15%)
  ],
  footer: align(left)[
    #text(size: 9pt, fill: gray)[$footertext
    #h(1fr)
    Created on #datetime.today().display()]
  ]
)

#set par(justify: true)
#set text(
  font: "Linux Libertine",
  size: 11pt,
)

#datetime.today().display("[month]/[day]/[year]")

#linebreak()

Attention: $medicaldirectorname

$insurancecompanyname

RE: Patient Name: $patientname

Policy Holder Name: $policyholdername

Patient ID \#: $patientid

Policy, Group, or Claim \#: $claimid 

#linebreak()
#linebreak()

Dear Madam/Sir:

This letter is to request approval for the surgery, hospital, and post-surgical care associated with $procedurename for $patientname.  
This patient is scheduled for surgery on $surgerydate.  
I have attached clinical documentation to support a determination of medical necessity for $procedurename.  

The $procedurename is clinically appropriate for my patient as $reasonsforappropriateness.  
In addition, your health plan’s coverage policy states that the $procedurename is considered medically necessary for patients with $riskfactors. 
The enclosed information supports the presence of these/this risk factors in my patient.  
Therefore, I have determined that $procedurename is justified. 

Based upon the above criteria and the information enclosed, I request that approval be granted for surgery for $patientname and all related services as soon as possible.  
Please fax your approval to my office at the following number $faxnumber or contact me with additional questions. 
I can be reached conveniently at $phonenumber. 

Sincerely,

#linebreak()
#linebreak()

$doctorname

$practicename

#linebreak()

Enclosures

- History and physical
- MD order and progress notes
- Pertinent test reports with written interpretation
