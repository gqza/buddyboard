// threads.js
// by lua (zav@tbdpowered.net)

function toggleContent(contentId, toggleElement) {
    $("." + contentId).toggle();

    var $toggle = $(toggleElement);
    $toggle.text( ($toggle.text() == '[-]' ? '[+]' : '[-]') );
}