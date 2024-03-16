curl -X POST http://127.0.0.1:8000/get_pdf_from_rawtypst \
     -H "Content-Type: application/json" \
     -d '{"source": "= Introduction\nIn this report, we will explore the various factors that influence _fluid dynamics_ in glaciers and how they contribute to the formation and behaviour of these natural structures.", "name": "hello"}' \
     -o test.pdf

