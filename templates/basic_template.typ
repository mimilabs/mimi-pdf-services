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
  size: 12pt,
)

$content

