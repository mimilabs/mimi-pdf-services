#set page(
  paper: "us-letter",
  header: align(right)[
    #image("mimilogo-withtext.png", width: 15%)
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
  size: 11pt,
)

= \$patientname - \$formname

\
= \$psection

\$profiledescription

#let frame(stroke) = (x, y) => (
  left: 0pt,
  right: 0pt,
  top: if y < 1 { stroke } else { 0pt },
  bottom: stroke,
)

#set table(
  fill: (rgb("ffebe2"), none, rgb("ffebe2"), none),
  stroke: frame(rgb("ddd")),
)
#table(
  columns: (auto, 1fr, auto, 1fr),
  [*\$pname1*], [\$pvalue1], [*\$pname2*], [\$pvalue2],
  [*\$pname3*], [\$pvalue3], [*\$pname4*], [\$pvalue4],
  [*\$pname5*], [\$pvalue5], [*\$pname6*], [\$pvalue6],
  [*\$pname7*], [\$pvalue7], [*\$pname8*], [\$pvalue8],
  [*\$pname9*], [\$pvalue9], [*\$pname10*], [\$pvalue10]  
)

\
= \$rsection

\$riskfactordescription

#let frame(stroke) = (x, y) => (
  left: 0pt,
  right: 0pt,
  top: if y < 2 { stroke } else { 0pt },
  bottom: stroke,
)

#set table(
  fill: (x, y) => if y < 1 { rgb("fffcdf") } else { none },
  stroke: frame(rgb("ddd")),
)

#table(
  columns: (auto, 1fr, 1fr, auto),
  table.header([*\$rname1a*],[*\$rname1b*],[*\$rname1c*],[*\$rname1d*]),
  [\$rvalue1a], [\$rvalue1b], [\$rvalue1c], [\$rvalue1d],
  [\$rvalue2a], [\$rvalue2b], [\$rvalue2c], [\$rvalue2d],
  [\$rvalue3a], [\$rvalue3b], [\$rvalue3c], [\$rvalue3d],
  [\$rvalue4a], [\$rvalue4b], [\$rvalue4c], [\$rvalue4d],
  [\$rvalue5a], [\$rvalue5b], [\$rvalue5c], [\$rvalue5d],  
  [\$rvalue6a], [\$rvalue6b], [\$rvalue6c], [\$rvalue6d],
  [\$rvalue7a], [\$rvalue7b], [\$rvalue7c], [\$rvalue7d],
  [\$rvalue8a], [\$rvalue8b], [\$rvalue8c], [\$rvalue8d],
  [\$rvalue9a], [\$rvalue9b], [\$rvalue9c], [\$rvalue9d],  
  [\$rvalue10a], [\$rvalue10b], [\$rvalue10c], [\$rvalue10d],
)

\
= \$csection

\$caregapdescription

#set table(
  fill: (x, y) => if y < 1 { rgb("edfde0") } else { none },
  stroke: frame(rgb("ddd")),
)

#table(
  columns: (auto, 1fr, 1fr, auto),
  table.header([*\$cname1a*],[*\$cname1b*],[*\$cname1c*],[*\$cname1d*]),
  [\$cvalue1a], [\$cvalue1b], [\$cvalue1c], [\$cvalue1d],
  [\$cvalue2a], [\$cvalue2b], [\$cvalue2c], [\$cvalue2d],
  [\$cvalue3a], [\$cvalue3b], [\$cvalue3c], [\$cvalue3d],
  [\$cvalue4a], [\$cvalue4b], [\$cvalue4c], [\$cvalue4d],
  [\$cvalue5a], [\$cvalue5b], [\$cvalue5c], [\$cvalue5d],  
)
