currentScroll = 0
previousScroll = 0
hide_override=false
function show_nav(nav) {
  nav.classList.remove("hide")
}
function hide_nav(nav) {
  nav.classList.add("hide")
}
function show_nav_by_name(name) {
  nav = document.querySelector('nav.' + name)
  show_nav(nav)
}
function hide_nav_by_name(name) {
  nav = document.querySelector('nav.' + name)
  hide_nav(nav)
}
function navigate_section() {
  hide_override=true
}
window.addEventListener("scroll", function() {
  if (hide_override) {
    hide_nav_by_name('site')
    hide_nav_by_name('reading')
    hide_nav_by_name('share')
    hide_nav_by_name('article')
    hide_nav_by_name('toc')
    hide_override=false
    return
  }
  h = window.innerHeight
  s = window.scrollY
  currentScroll = s
  site_nav = document.querySelector('nav.site')
  article_nav = document.querySelector('nav.article')
  reading_nav = document.querySelector('nav.reading')
  share_nav = document.querySelector('nav.share')
  if ( s > h && currentScroll > previousScroll ) {
    hide_nav(site_nav)
    hide_nav(article_nav)
    show_nav(reading_nav)
    show_nav(share_nav)
  }
  else {
    show_nav(site_nav)
    show_nav(article_nav)
    hide_nav(reading_nav)
    hide_nav(share_nav)
  }

  sections = document.getElementsByTagName("section")
  cur_sec = 0
  for(i=0; i<sections.length; i++) {
    if (s >= sections[i].offsetTop) {
      cur_sec = i
    }
  }
  reading_nav.getElementsByClassName("title")[0].innerHTML = sections[cur_sec].getElementsByTagName("h1")[0].innerHTML

  previousScroll = currentScroll
})
window.addEventListener('load', function() {
  function link_html( link_hash, link_text ) {
    return "<li><a onclick='navigate_section()' href='#" + link_hash + "''>" + link_text + "</a></li>"
  }
  toc_nav = document.querySelector('nav.toc .sections_list')
  sections = document.querySelectorAll('article section')
  toc = toc_nav.innerHTML + "<ul>"
  for (i=1; i<sections.length; i++) {
    toc += link_html( 
      sections[i].id,
      sections[i].querySelector('h1').innerHTML )
  }
  toc += "</ul>"
  toc_nav.innerHTML = toc
})