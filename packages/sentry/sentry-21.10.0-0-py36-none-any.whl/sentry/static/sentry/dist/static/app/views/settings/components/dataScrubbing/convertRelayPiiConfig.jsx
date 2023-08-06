Object.defineProperty(exports, "__esModule", { value: true });
const types_1 = require("./types");
// Remap PII config format to something that is more usable in React. Ideally
// we would stop doing this at some point and make some updates to how we
// store this configuration on the server.
//
// For the time being the PII config format is documented at
// https://getsentry.github.io/relay/pii-config/
function convertRelayPiiConfig(relayPiiConfig) {
    const piiConfig = relayPiiConfig ? JSON.parse(relayPiiConfig) : {};
    const rules = piiConfig.rules || {};
    const applications = piiConfig.applications || {};
    const convertedRules = [];
    for (const application in applications) {
        for (const rule of applications[application]) {
            const resolvedRule = rules[rule];
            const id = convertedRules.length;
            const source = application;
            if (!resolvedRule) {
                // Convert a "built-in" rule like "@anything:remove" to an object {
                //   type: "anything",
                //   method: "remove"
                // }
                if (rule[0] === '@') {
                    const typeAndMethod = rule.slice(1).split(':');
                    let [type] = typeAndMethod;
                    const [, method] = typeAndMethod;
                    if (type === 'urlauth')
                        type = 'url_auth';
                    if (type === 'usssn')
                        type = 'us_ssn';
                    convertedRules.push({
                        id,
                        method: method,
                        type: type,
                        source,
                    });
                }
                continue;
            }
            const { type, redaction } = resolvedRule;
            const method = redaction.method;
            if (method === types_1.MethodType.REPLACE && resolvedRule.type === types_1.RuleType.PATTERN) {
                convertedRules.push({
                    id,
                    method: types_1.MethodType.REPLACE,
                    type: types_1.RuleType.PATTERN,
                    source,
                    placeholder: redaction === null || redaction === void 0 ? void 0 : redaction.text,
                    pattern: resolvedRule.pattern,
                });
                continue;
            }
            if (method === types_1.MethodType.REPLACE) {
                convertedRules.push({
                    id,
                    method: types_1.MethodType.REPLACE,
                    type,
                    source,
                    placeholder: redaction === null || redaction === void 0 ? void 0 : redaction.text,
                });
                continue;
            }
            if (resolvedRule.type === types_1.RuleType.PATTERN) {
                convertedRules.push({
                    id,
                    method,
                    type: types_1.RuleType.PATTERN,
                    source,
                    pattern: resolvedRule.pattern,
                });
                continue;
            }
            convertedRules.push({ id, method, type, source });
        }
    }
    return convertedRules;
}
exports.default = convertRelayPiiConfig;
//# sourceMappingURL=convertRelayPiiConfig.jsx.map