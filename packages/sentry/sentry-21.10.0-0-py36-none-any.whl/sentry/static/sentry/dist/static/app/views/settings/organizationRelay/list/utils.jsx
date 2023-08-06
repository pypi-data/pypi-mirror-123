Object.defineProperty(exports, "__esModule", { value: true });
exports.getShortPublicKey = exports.getRelaysByPublicKey = void 0;
/**
 * Convert list of individual relay objects into a per-file summary grouped by publicKey
 */
function getRelaysByPublicKey(relays, relayActivities) {
    return relays.reduce((relaysByPublicKey, relay) => {
        const { name, description, created, publicKey } = relay;
        if (!relaysByPublicKey.hasOwnProperty(publicKey)) {
            relaysByPublicKey[publicKey] = { name, description, created, activities: [] };
        }
        if (!relaysByPublicKey[publicKey].activities.length) {
            relaysByPublicKey[publicKey].activities = relayActivities.filter(activity => activity.publicKey === publicKey);
        }
        return relaysByPublicKey;
    }, {});
}
exports.getRelaysByPublicKey = getRelaysByPublicKey;
/**
 * Returns a short publicKey with only 20 characters
 */
function getShortPublicKey(publicKey) {
    return publicKey.substring(0, 20);
}
exports.getShortPublicKey = getShortPublicKey;
//# sourceMappingURL=utils.jsx.map