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
    //hide_nav_by_name('article')
    hide_nav_by_name('toc')
    hide_override=false
    return
  }
  h = window.innerHeight
  s = window.scrollY
  currentScroll = s
  site_nav = document.querySelector('nav.site')
  //article_nav = document.querySelector('nav.article')
  reading_nav = document.querySelector('nav.reading')
  share_nav = document.querySelector('nav.share')
  if ( s > h && currentScroll > previousScroll ) {
    hide_nav(site_nav)
    //hide_nav(article_nav)
    show_nav(reading_nav)
    show_nav(share_nav)
  }
  else {
    show_nav(site_nav)
    //show_nav(article_nav)
    hide_nav(reading_nav)
    hide_nav(share_nav)
  }

  previousScroll = currentScroll
})
