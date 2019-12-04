(function() {
  var button, buttonStyles, materialIcons;

  materialIcons = '<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">';
  buttonStyles = '<link href="/static/css/auth/bstyle.css" rel="stylesheet">';
  button = '<a href="#" class="at-button"><i class="material-icons">link</i></a>';

  document.body.innerHTML += materialIcons + buttonStyles + button;

}).call(this);