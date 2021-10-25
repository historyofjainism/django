window.onload = function() {
    timeline_bar = document.createElement('div')
    timeline_bar.className = 'timeline__bar'
    article_dom = document.getElementsByTagName('article')[0]
    article_dom.insertBefore(timeline_bar, article_dom.firstChild)
}
