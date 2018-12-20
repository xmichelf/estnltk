var elements = document.getElementsByClassName("overlapping-span")
for (let i = 0; i < elements.length; i++){
    elements.item(i).addEventListener("click",function() {intermediate_table(elements.item(i));})
}

function intermediate_table(span_element) {
    console.log(span_element)
    let spantable = document.createElement('div')
    spantable.classList.add('tables')
    spantable.innerHTML = span_table(span_element)
    span_element.parentElement.appendChild(spantable)

    //Position the element below the text
    spantable.style.left = "0px";
    spantable.style.top = "0px";
    spantable.style.left = span_element.getBoundingClientRect().left-spantable.getBoundingClientRect().left + 'px'
    spantable.style.top = span_element.getBoundingClientRect().top-spantable.getBoundingClientRect().top+span_element.getBoundingClientRect().height+ 'px'
    spantable.parentElement.style.height = spantable.parentElement.style.height+"100px"

    spantable.addEventListener('click', function () {
        let element = this.parentElement
        element.removeChild(this)  //deleting the table
    })
}

function span_table (span) {{
    data = span.getAttribute("span_info")
    data = data.split(",")
    var content = '<table>'
    for (let row of data) {
        content+='<tr><td>'
        content+=row
        content+='</td></tr>'
    }
    content += '</table>'

    return content
}}