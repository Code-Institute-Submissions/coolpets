var _0x507d=["\x70\x6B\x5F\x74\x65\x73\x74\x5F\x35\x31\x47\x75\x56\x41\x35\x46\x4F\x6C\x6B\x58\x67\x56\x58\x4F\x69\x4F\x33\x68\x61\x52\x55\x35\x56\x54\x68\x6C\x5A\x38\x64\x66\x66\x46\x37\x59\x30\x46\x6F\x7A\x4F\x30\x43\x66\x63\x75\x48\x41\x6D\x69\x6F\x41\x64\x57\x4E\x39\x34\x61\x44\x32\x33\x6C\x41\x74\x79\x32\x6E\x67\x47\x52\x57\x61\x58\x6B\x51\x72\x69\x74\x43\x54\x51\x32\x47\x73\x39\x30\x42\x75\x66\x30\x30\x31\x56\x32\x36\x64\x59\x57\x7A"];var stripe=Stripe(_0x507d[0])

$('#submit-payment-btn').click(function () {
    startCheckout();
});

/**
 * Activates stripe v3 checkout page
 */
async function startCheckout() {
    const { error } = await stripe.redirectToCheckout({
        sessionId: s_id
    });

    if (error) {
        alert('Something went wrong with the payment, please try again.');
    }
}