Object.defineProperty(exports, "__esModule", { value: true });
exports.findMatchedRules = void 0;
/**
 * Given a list of rule objects returned from the API, locate the matching
 * rules for a specific owner.
 */
function findMatchedRules(rules, owner) {
    if (!rules) {
        return undefined;
    }
    const matchOwner = (actorType, key) => (actorType === 'user' && key === owner.email) ||
        (actorType === 'team' && key === owner.name);
    const actorHasOwner = ([actorType, key]) => actorType === owner.type && matchOwner(actorType, key);
    return rules
        .filter(([_, ruleActors]) => ruleActors.find(actorHasOwner))
        .map(([rule]) => rule);
}
exports.findMatchedRules = findMatchedRules;
//# sourceMappingURL=findMatchedRules.jsx.map