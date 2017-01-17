;(function(window, document) {

  // Hide body until we're done fiddling with the DOM
  document.body.style.display = 'none';

  //////////////////////////////////////////////////////////////////////
  //
  // Markdown!
  //

  // Generate Markdown
  var html = marked(document.getElementsByTagName('xmp')[0].innerHTML);
  document.getElementById('content').innerHTML = html;
  document.getElementsByTagName('xmp')[0].innerHTML = '';

  // Prettify
  var codeEls = document.getElementsByTagName('code');
  for (var i=0, ii=codeEls.length; i<ii; i++) {
    var codeEl = codeEls[i];
    var lang = codeEl.className;
    codeEl.className = 'prettyprint lang-' + lang;
  }
  prettyPrint();

  // Style tables
  var tableEls = document.getElementsByTagName('table');
  for (var i=0, ii=tableEls.length; i<ii; i++) {
    var tableEl = tableEls[i];
    tableEl.className = 'table table-striped table-bordered';
  }

  // All done - show body
  document.body.style.display = '';

})(window, document);