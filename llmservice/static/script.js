['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  document.addEventListener(eventName, function (e) {
    e.preventDefault();
    e.stopPropagation();
  }, false);
});

document.addEventListener('drop', e=>handleFiles(e.dataTransfer.files), false);

function handleFiles(files){
  for (let file of files) {handleFile(file)}
}

function handleFile(file) {handleDocument(file)}

const ML_api = `http://${window.location.host}/`;

class Document{
  constructor(file, type, date, title){
    this.uuid = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    this.file = file;
    this.type = type;
    this.date = date;
    this.title = title;
    this.element = document.createElement('tr');
    this.update();  
  }

  update() {this.element.innerHTML = `<td><a href="/cloud/view/${this.uuid}">open</a> ${this.title}</td><td>${this.date}</td><td>${this.type}</td>`}
}

docs_list = [];
function add_doc(doc){
  docs_list.push(doc);
  document.querySelector('#gallery>table').appendChild(doc.element);
}

// add_doc(new Document('file', 'type', 'date', 'title'));

loadr = '<span class="loading">...</span>';

function handleDocument(file){
  
  let newDoc = new Document(file, loadr, loadr, loadr);
  add_doc(newDoc);

  let formData = new FormData();
  formData.append('file', file);


  fetch(ML_api+"pdf_api/handle_pdf", {
    method: 'POST',
    body: formData,
  }).then(response => response.json().then(data => {
    let text = data.text
    console.log({text})

    fetch(ML_api+"llm_api/extract_invoice_information", {
      method: 'POST',
      body: JSON.stringify({
        text: text,
        required_fields: ["Datum", "Dokument Typ", "Titel", "Zusammenfassung"],
        optional_fields: ["Betrag", "Rechnungsnummer", "Kundennummer", "Assoziierte Personen"],
        additional_prompt: 'Wenn kein Datum gegeben ist, setze es auf NA ansonsten gib es im format 30.12.2020 an. Wenn kein Tag gegeben ist setze es auf 01.\nIn der Zusammenfassung gib eine Beschreibung des Dokuments an in einem Satz an.'
      }),
      headers: {'Content-Type': 'application/json'}
    }).then(response => response.json().then(data => {
      data = JSON.parse(data);
      console.log(data)
      newDoc.type = data["Dokument Typ"];
      newDoc.date = data["Datum"];
      newDoc.title = data["Titel"];
      newDoc.update();
    }));
  }));
}