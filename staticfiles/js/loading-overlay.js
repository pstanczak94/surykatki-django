
function ShowLoadingOverlay(text) {
	if ($('div.loading').length <= 0) {
		$('body').append(
			'<div class="loading">' +
			 '<div class="loading-inner">' +
			  '<div class="loading-spinner"></div>' +
			  '<div class="loading-text">' + text + '</div>' +
			 '</div>' +
			'</div>'
		);
	}
	
	$('div.loading').stop().fadeTo('slow', 1.0);
	
	$(window).keydown(function(e) {
		if ($('div.loading').length > 0) {
			if (e.keyCode == 27) {
				HideLoadingOverlay();
				e.preventDefault();
			}
		}
	});
}

function HideLoadingOverlay() {
	if ($('div.loading').length > 0) {
		$('div.loading').stop().fadeTo('slow', 0.0, function() {
			$('div.loading').remove();
		});
	}
}