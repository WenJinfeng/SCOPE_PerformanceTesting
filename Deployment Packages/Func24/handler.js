'use strict';

module.exports.main = function(event, context, callback) {
    console.log('Function publish running.');

    if (event.approved == 'true') {
	const purchaseEvent = {
	    productId: event.id,
	    productPrice: event.price,
	    userId: event.user,
	    authorization: event.authorization,
	    devFinished: 'false: might actually be finished.'
	};

	callback(null, purchaseEvent);
    } else {
	var purchaseEvent = {
	    devFinished: 'false: might actually be finished.'
	};

	if (typeof event.failureReason === 'string' || event.failureReason instanceof String) {
	    purchaseEvent.failureReason = event.failureReason;
	} else {
	    purchaseEvent.failureReason = {...event.failureReason};
	}

	callback(null, purchaseEvent);
    }
}
