// Adopted from https://www.merckaccessprogram-zinplava.com/static/pdf/zinplava-sample-prior-authorization-letter.pdf

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

I am writing to request authorization for $productname for my patient, $patientname.  
I have prescribed $productname because this patient has been diagnosed with $diagnosis, and I believe that therapy with $productname is appropriate for this patient.  
Attached to this request are clinical notes regarding this patient’s disease state, the FDA approval letter for $productname, and the $productname package insert. 

$productname is indicated for $indications. 

$reasonsforappropriateness 

Thank you for taking the time to read this letter. I look forward to your prompt review of this request. 

#linebreak()

Best regards,

$doctorname

$practicename

#linebreak()
#linebreak()

Enclosures

- $productname FDA approval letter
- $productname package insert
- Patient clinical notes and other relevant supporting documentation
