
function randomPrice() {
    var cents = Math.floor(Math.random() * 100);
    var dollars = Math.floor(Math.random() * 100);

    return (dollars + (cents * .01)).toFixed(2);
}


module.exports.main = function(event, context, callback) {
    console.log('Function getPrice running.');

    console.log(event.id);

    if (Math.random() < 0.9) {
        const response = {
	    gotPrice: 'true',
	    price: randomPrice(),
	    devFinished: 'false: does not use database, generates random price.'
	};
    // console.log(response);
	callback(null, response);
    } else {
	const response = {
	    gotPrice: 'false',
	    failureReason: 'No price in the catalog',
	    devFinished: 'false'
	};
    // console.log(response);
	callback(null, response);
    }
}
// var event1 = {"id":6}
// main(event1,"","")
