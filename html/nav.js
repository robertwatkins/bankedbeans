function writenav(){
    var navigation = document.getElementById("nav");
    navigation.appendChild(link("Update Memo field for transactions without category","updatememo.html", "large"));
    navigation.appendChild(document.createTextNode(" "));
    navigation.appendChild(link("List Current Year Category Totals","categorytotals.html","medium"));
    navigation.appendChild(document.createTextNode(" "));
    navigation.appendChild(link("List Current Year transactions","updatememo.html?source=any&year=currentyear&category=any","medium"));
    navigation.appendChild(document.createTextNode(" "));
    navigation.appendChild(link("List Assignemnet Rules","rules.html","medium"));
    navigation.appendChild(document.createElement('br'));
    navigation.appendChild(document.createElement('br'));
}

function link(title, link, size){
    var a = document.createElement('a');
    var linkText = document.createTextNode(title);
    a.appendChild(linkText);
    a.title = title;
    a.href = link;
    a.classList.add('button-'+size);
    return a
}