#set page(
  paper: "us-letter",
  header: align(right)[
    #image("mimilabs-withtext.png", width: 15%)
  ],
  footer: align(left)[
    #text(size: 9pt, fill: gray)[miilabs.ai - Beautiful Small Projects, One by One
    #h(1fr)
    Created on #datetime.today().display()]
  ]
)

#set par(justify: true)
#set text(
  font: "Linux Libertine",
  size: 12pt,
)

$content

