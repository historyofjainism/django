function navigate_section() {
    hide_override=true
}
window.addEventListener("scroll", function() {

    sections = document.getElementsByTagName("section")
    cur_sec = 0
    for(i=0; i<sections.length; i++) {
      if (s >= sections[i].offsetTop) {
        cur_sec = i
      }
    }
    reading_nav.getElementsByClassName("title")[0].innerHTML = sections[cur_sec].getElementsByTagName("h1")[0].innerHTML
  
})
window.addEventListener('load', function() {
    function link_html( link_hash, link_text ) {
      return "<li><a onclick='navigate_section()' href='#" + link_hash + "''>" + link_text + "</a></li>"
    }
    toc_nav = document.querySelector('nav.toc .sections_list')
    sections = document.querySelectorAll('article section')
    toc = toc_nav.innerHTML + "<ul>"
    for (i=0; i<sections.length; i++) {
      toc += link_html( 
        sections[i].id,
        sections[i].querySelector('h1').innerHTML )
    }
    toc += "</ul>"
    toc_nav.innerHTML = toc
})